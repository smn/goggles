from twisted.internet.defer import inlineCallbacks, returnValue, maybeDeferred
from twisted.trial.unittest import TestCase
from twisted.web.test.test_web import DummyRequest

from goggles.helper import ImportJobHelper
from goggles.service import DBConnection


class GoggleTestCase(TestCase):

    timeout = 5

    SAMPLE_INBOUND_USER_MESSAGE = {
        "transport_name": "ussd_transport",
        "group": None,
        "from_addr": "27123456789",
        "timestamp": "2014-09-10 05:44:20.724588",
        "provider": None,
        "to_addr": "*123*456#",
        "content": None,
        "routing_metadata": {},
        "message_version": "20110921",
        "transport_type": "ussd",
        "helper_metadata": {},
        "in_reply_to": None,
        "session_event": "new",
        "message_id": "00000a9631bb4515b82381b38a0766a0",
        "message_type": "user_message"
    }

    SAMPLE_OUTBOUND_USER_MESSAGE = {
        "transport_name": "ussd_transport",
        "transport_metadata": {},
        "group": None,
        "from_addr": "*123*456#",
        "timestamp": "2014-09-26 17:49:29.630470",
        "provider": None,
        "to_addr": "27760166203",
        "content": (
            "Only give medicine that your health worker recommends. "
            "After he recovers, give him and extra feed or meal every "
            "day for a\n1. More\n2. Back\n3. Send to me by SMS"),
        "routing_metadata": {},
        "message_version": "20110921",
        "transport_type": "ussd",
        "helper_metadata": {},
        "in_reply_to": "00000a9631bb4515b82381b38a0766a0",
        "session_event": None,
        "message_id": "00000780b3e0420290da70ba2faabd43",
        "message_type": "user_message"
    }

    def setup_test_db(self, db_name='goggles'):
        test_db_name = 'test_tx_%s' % (db_name,)
        conn = DBConnection()
        d = conn.connect('dbname=%s' % (db_name,))
        d.addCallback(lambda _: conn.runOperation("""
            CREATE DATABASE %s
            WITH
                ENCODING = 'UTF8'
                OWNER = DEFAULT
                TEMPLATE = template0
            """ % (test_db_name,)))
        d.addCallback(lambda _: test_db_name)

        # cleanup db when done
        self.addCleanup(conn.close)
        self.addCleanup(
            conn.runOperation,
            """
            DROP DATABASE
            IF EXISTS
            %s
            """ % (test_db_name,))
        return d

    def connect_test_db(self):
        conn = DBConnection()
        d = self.setup_test_db()
        d.addCallback(lambda db_name: conn.connect('dbname=%s' % (db_name,)))
        d.addCallback(lambda _: self.addCleanup(conn.close))
        d.addCallback(lambda _: conn)
        return d

    def make_request(self, path='', user='user-id'):
        request = DummyRequest([path])
        request.getUser = lambda: user
        return request

    def create_import_job(self, conn, username, password):
        def ix(cursor):
            d = cursor.execute(
                """
                INSERT INTO warehouse_importjob
                    (username_token, password_token)
                VALUES (%s, %s)
                RETURNING id
                """, (username, password))
            d.addCallback(lambda c: c.fetchone()[0])
            return d

        return conn.runInteraction(ix)

    @inlineCallbacks
    def make_job_helper(self, conn=None, username='foo', password='bar'):
        conn = conn or (yield self.connect_test_db())
        job_id = yield self.create_import_job(conn, username, password)
        returnValue(ImportJobHelper(conn, job_id))
