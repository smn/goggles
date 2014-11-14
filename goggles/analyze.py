import sys
import csv
import iso8601


from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet import protocol

from txredis.client import HiRedisClient

from goggles.main import mk_key, session_key


def calc_seconds(info):
    start = info.get('start')
    stop = info.get('stop')
    if not all([start, stop]):
        return

    start = iso8601.parse_date(start)
    stop = iso8601.parse_date(stop)
    delta = stop - start
    return delta.total_seconds()


@inlineCallbacks
def run(redis_host='127.0.0.1', redis_port=6379, redis_db=8):

    clientCreator = protocol.ClientCreator(reactor, HiRedisClient)
    redis = yield clientCreator.connectTCP(redis_host, redis_port)
    yield redis.select(redis_db)

    mnos = yield redis.smembers(mk_key('mnos'))

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=[
            'session_id',
            'mno',
            'ussd_code',
            'start',
            'stop',
            'seconds',
            'is_faq',
        ])

    for mno in mnos:
        yield handle_mno(writer, redis, mno)

    reactor.stop()


@inlineCallbacks
def handle_mno(writer, redis, mno):
    session_ids = yield redis.smembers(mk_key('mnos', mno, 'session_ids'))
    for session_id in session_ids:
        session_info = yield redis.hgetall(session_key(mno, session_id))
        writer.writerow({
            'session_id': session_id,
            'mno': mno,
            'ussd_code': session_info.get('ussd_code'),
            'start': session_info.get('start'),
            'stop': session_info.get('stop'),
            'seconds': calc_seconds(session_info),
            'is_faq': session_info.get('is_faq'),
        })


if __name__ == '__main__':

    run()
    reactor.run()
