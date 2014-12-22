import django
django.setup()

from django.conf import settings
from django.test import utils

from goggles.service import DBConnection


class DjangoTestMixin(object):

    def setup_test_django_db(self):
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

    def connect_test_django_db(self):
        db_name = self.setup_test_django_db()
        conn = DBConnection()
        d = conn.connect('dbname=%s' % (db_name,))
        d.addCallback(lambda _: self.addCleanup(conn.close))
        d.addCallback(lambda _: conn)
        return d
