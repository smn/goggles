import json
import sys
from datetime import datetime

from twisted.python import log
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.protocol import Factory
from twisted.internet import protocol
from twisted.internet.endpoints import TCP4ServerEndpoint

from txredis.client import HiRedisClient


# This is the date format we work with internally
VUMI_DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class GoggleProtocol(LineReceiver):

    delimiter = '\n'

    def __init__(self, factory):
        self.factory = factory

    def lineReceived(self, line):
        self.factory.handle_data(json.loads(line))


def mk_key(*args):
    return '#'.join(args)


def rget(data, key):
    parts = key.split('.')
    if len(parts) > 1:
        return rget(data[parts[0]], '.'.join(parts[1:]))
    return data[parts[0]]


def session_key(mno, session_id):
    return mk_key('mnos', mno, 'session_id', session_id)


def is_faq(content):
    faq_bits = [
        'We have gathered information in the areas below. Please select:',
        'Please select one:',
        'Send to me by SMS',
        'Stuur na my as SMS',
    ]
    return any([bit in content for bit in faq_bits])


class GoggleFactory(Factory):

    protocol = GoggleProtocol

    def __init__(self, redis):
        self.redis = redis

    def handle_data(self, data):
        direction = ('inbound'
                     if data['to_addr'].startswith('*')
                     else 'outbound')
        fn = getattr(self, 'handle_%s_data' % (direction,))
        print direction, data['message_id']
        return fn(data)

    def save_msg_bit(self, data, key):
        r_key = mk_key('msg', data['message_id'])
        r_value = rget(data, key)
        return self.redis.hset(r_key, key, r_value)

    def load_msg_bits(self, message_id):
        r_key = mk_key('msg', message_id)
        return self.redis.hgetall(r_key)

    @inlineCallbacks
    def handle_inbound_data(self, data):
        mno = rget(data, 'transport_metadata.aat_ussd.provider')
        session_id = rget(data, 'transport_metadata.aat_ussd.ussd_session_id')
        session_event = rget(data, 'session_event')
        timestamp = rget(data, 'timestamp')

        yield self.redis.sadd(mk_key('mnos'), mno)
        yield self.redis.sadd(mk_key('mnos', mno, 'session_ids'), session_id)

        yield self.redis.hset(
            session_key(mno, session_id),
            'ussd_code',
            data['to_addr'])

        if session_event == 'new':
            yield self.redis.hset(
                session_key(mno, session_id),
                'start',
                datetime.strptime(timestamp, VUMI_DATE_FORMAT).isoformat())

    @inlineCallbacks
    def handle_outbound_data(self, data):

        in_reply_to = rget(data, 'in_reply_to')
        if in_reply_to is None:
            return

        mno = rget(data, 'transport_metadata.aat_ussd.provider')
        session_id = rget(data, 'transport_metadata.aat_ussd.ussd_session_id')
        session_event = rget(data, 'session_event')
        timestamp = rget(data, 'timestamp')

        yield self.redis.sadd(mk_key('mnos'), mno)
        yield self.redis.sadd(mk_key('mnos', mno, 'session_ids'), session_id)

        yield self.redis.hset(
            session_key(mno, session_id),
            'is_faq', is_faq(rget(data, 'content')))

        if session_event == 'close':
            yield self.redis.hset(
                session_key(mno, session_id),
                'stop',
                datetime.strptime(timestamp, VUMI_DATE_FORMAT).isoformat())

    def buildProtocol(self, addr):
        return GoggleProtocol(self)


@inlineCallbacks
def run(port, redis_host='127.0.0.1', redis_port=6379, redis_db=8):

    clientCreator = protocol.ClientCreator(reactor, HiRedisClient)
    redis = yield clientCreator.connectTCP(redis_host, redis_port)
    yield redis.select(redis_db)

    endpoint = TCP4ServerEndpoint(reactor, port)
    endpoint.listen(GoggleFactory(redis))


if __name__ == '__main__':

    log.startLogging(sys.stdout)

    run(8007)
    reactor.run()
