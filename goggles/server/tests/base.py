from twisted.trial.unittest import TestCase

from goggles.service import DBConnection


class GoggleTestCase(TestCase):

    timeout = 5

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
