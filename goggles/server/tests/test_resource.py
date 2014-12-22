import json

from StringIO import StringIO

from goggles.helper import ImportJobHelper
from goggles.server.tests.base import GoggleTestCase
from goggles.server.tests.django_base import DjangoTestMixin
from goggles.server.resource import GoggleResource, UserMessageResource
from goggles.service import GoggleServerRealm
from goggles.server.auth import GoggleCredentialsChecker

from twisted.cred import portal
from twisted.internet.defer import inlineCallbacks, succeed
from twisted.web import server
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


class TestUserMessageResource(GoggleTestCase, DjangoTestMixin):

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
        job = yield self.make_job_helper(conn=conn)
        resource = UserMessageResource(job, 'inbound')
        response = yield self.post_data(resource, sample)
        [message] = yield job.fetch_user_messages()
        self.assertEqual(message['message_id'], sample['message_id'])

    @inlineCallbacks
    def test_import_bad_job_id(self):
        conn = yield self.connect_test_django_db()
        job = ImportJobHelper(conn, 'invalid_job_id')
        resource = UserMessageResource(job, 'inbound')
        response = yield self.post_data(
            resource, self.SAMPLE_INBOUND_USER_MESSAGE)
        [error] = response.written
        self.assertTrue('invalid input syntax for integer' in error)

    @inlineCallbacks
    def test_import_bad_db_connection(self):
        job = ImportJobHelper(None, 'invalid_job_id')
        resource = UserMessageResource(job, 'inbound')
        response = yield self.post_data(
            resource, self.SAMPLE_INBOUND_USER_MESSAGE)
        [error] = response.written
        self.assertTrue(
            "'NoneType' object has no attribute 'runQuery'" in error)
