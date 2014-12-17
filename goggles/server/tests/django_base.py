import django
django.setup()

from django.conf import settings
from django.test import utils

from goggles.service import DBConnection
from goggles.server.tests.base import GoggleTestCase


class DjangoGoggleTestCase(GoggleTestCase):

    def setup_test_db(self):
        """
        Setup the Django test database and return the name of the test
        database
        """
        runner_class = utils.get_runner(settings)
        runner = runner_class(verbosity=False, interactive=False)
        runner.setup_test_environment()
        old_config = runner.setup_databases()
        self.addCleanup(runner.teardown_databases, old_config)
        self.addCleanup(runner.teardown_test_environment)
        return settings.DATABASES['default']['NAME']

    def connect_test_db(self):
        db_name = self.setup_test_db()
        conn = DBConnection()
        d = conn.connect('dbname=%s' % (db_name,))
        d.addCallback(lambda _: self.addCleanup(conn.close))
        d.addCallback(lambda _: conn)
        return d

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
