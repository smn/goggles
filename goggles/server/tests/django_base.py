from StringIO import StringIO

import django
django.setup()

from django.test import SimpleTestCase

import pytest

from twisted.internet.defer import inlineCallbacks, returnValue


@pytest.mark.twisted_django
class DjangoTestMixin(SimpleTestCase):

    @inlineCallbacks
    def connect_test_django_db(self):
        """
        NOTE:   This is a shortcut to what the Django `migrate` management
                command does. It will only work if Django is made to believe
                that none of the apps do migrations.

                We do this by having `test_settings` point at something
                not migrations-y in the MIGRATION_MODELS
        """
        conn = yield self.connect_test_db()
        from django.core.management import call_command
        from django.apps import apps

        # Order here is apparently important, I don't know how Django
        # figures out the order internally.
        core_apps = [
            'contenttypes',
            'auth',
            'admin',
        ]
        for app_config in apps.get_app_configs():
            if app_config.label not in core_apps:
                core_apps.append(app_config.label)

        for app in core_apps:
            stdout = StringIO()
            call_command('sqlall', app, no_color=True, stdout=stdout)
            sql = stdout.getvalue()
            if sql:
                yield conn.runOperation(sql)
        returnValue(conn)
