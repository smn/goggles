import json

from StringIO import StringIO

from goggles.helper import ImportJobHelper
from goggles.server.tests.base import GoggleTestCase
from goggles.server.tests.django_base import DjangoTestMixin
from goggles.server.resource import (
    GoggleResource, UploadUserMessageResource, DownloadUserMessageResource)
from goggles.service import GoggleServerRealm
from goggles.server.auth import GoggleCredentialsChecker

from twisted.cred import portal
from twisted.internet.defer import inlineCallbacks, succeed
from twisted.web.guard import BasicCredentialFactory, HTTPAuthSessionWrapper


class TestGoggleResource(GoggleTestCase):

    @inlineCallbacks
    def setUp(self):
        self.conn = yield self.connect_test_db()
        self.resource = GoggleResource(self.conn)

    def test_authenticated_resource(self):
        checker = GoggleCredentialsChecker(self.conn)
        realm = GoggleServerRealm(self.conn, GoggleResource)
        p = portal.Portal(realm, [checker])
        credentialFactory = BasicCredentialFactory("Goggles")
        protected_resource = HTTPAuthSessionWrapper(p, [credentialFactory])
        req = self.make_request()
        protected_resource.render(req)
        self.assertEqual(
            req.responseHeaders.getRawHeaders('www-authenticate'),
            ['basic realm="Goggles"'])


class TestUploadUserMessageResource(GoggleTestCase, DjangoTestMixin):

    def post_data(self, resource, data):
        request = self.make_request()
        request.content = StringIO(json.dumps(data))
        resource.render_POST(request)
        if request.finished:
            return succeed(request)

        d = request.notifyFinish()
        d.addCallback(lambda _: request)
        return d

    @inlineCallbacks
    def test_import(self):
        sample = self.SAMPLE_INBOUND_USER_MESSAGE
        conn = yield self.connect_test_django_db()
        job_helper = yield self.make_job_helper(conn=conn)
        resource = UploadUserMessageResource(job_helper, 'inbound')
        yield self.post_data(resource, sample)
        [message] = yield job_helper.fetch_user_messages()
        self.assertEqual(message['message_id'], sample['message_id'])

    @inlineCallbacks
    def test_import_bad_job_id(self):
        conn = yield self.connect_test_django_db()
        job_helper = ImportJobHelper(conn, 'invalid_job_id')
        resource = UploadUserMessageResource(job_helper, 'inbound')
        response = yield self.post_data(
            resource, self.SAMPLE_INBOUND_USER_MESSAGE)
        [error] = response.written
        self.assertTrue('invalid input syntax for integer' in error)

    @inlineCallbacks
    def test_import_bad_db_connection(self):
        job_helper = ImportJobHelper(None, 'invalid_job_id')
        resource = UploadUserMessageResource(job_helper, 'inbound')
        response = yield self.post_data(
            resource, self.SAMPLE_INBOUND_USER_MESSAGE)
        [error] = response.written
        self.assertTrue(
            "'NoneType' object has no attribute 'runQuery'" in error)


class TestDownloadUserMessageResource(GoggleTestCase, DjangoTestMixin):

    def get_data(self, resource):
        request = self.make_request()
        resource.content = StringIO('')
        resource.render_GET(request)
        if request.finished:
            return succeed(request)

        d = request.notifyFinish()
        d.addCallback(lambda _: request)
        return d

    @inlineCallbacks
    def test_download_inbound(self):
        conn = yield self.connect_test_django_db()
        job_helper = yield self.make_job_helper(conn=conn)
        resource = DownloadUserMessageResource(job_helper, 'inbound')
        response = yield self.get_data(resource)
        print response.responseCode
        print '%s' % (response.written,)
