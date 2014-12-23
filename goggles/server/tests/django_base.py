from StringIO import StringIO

import django
django.setup()

from twisted.internet.defer import inlineCallbacks, returnValue


class DjangoTestMixin(object):

    @inlineCallbacks
    def connect_test_django_db(self):
        conn = yield self.connect_test_db()
        from django.core.management import call_command
        from django.apps import apps

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
