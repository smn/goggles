from goggles.server.tests.base import GoggleTestCase
from goggles.server.tests.django_base import DjangoTestMixin
from goggles.server.auth import GoggleCredentialsChecker, GoggleServerRealm
from goggles.server.resource import UploadResource

from twisted.cred.credentials import UsernamePassword
from twisted.cred.error import UnauthorizedLogin
from twisted.internet.defer import inlineCallbacks
from twisted.web.resource import IResource


class TestAuth(GoggleTestCase, DjangoTestMixin):

    @inlineCallbacks
    def test_valid_credentials(self):
        conn = yield self.connect_test_django_db()
        job_id = yield self.create_import_job(
            conn, username='foo', password='bar')
        checker = GoggleCredentialsChecker(conn)
        creds = UsernamePassword('foo', 'bar')
        resp = yield checker.requestAvatarId(creds)
        self.assertEqual(resp, job_id)

    @inlineCallbacks
    def test_invalid_username(self):
        conn = yield self.connect_test_django_db()
        yield self.create_import_job(
            conn, username='foo', password='bar')
        checker = GoggleCredentialsChecker(conn)
        creds = UsernamePassword('bar', 'baz')
        yield self.assertFailure(
            checker.requestAvatarId(creds), UnauthorizedLogin)

    @inlineCallbacks
    def test_invalid_password(self):
        conn = yield self.connect_test_django_db()
        yield self.create_import_job(
            conn, username='foo', password='bar')
        checker = GoggleCredentialsChecker(conn)
        creds = UsernamePassword('foo', 'baz')
        yield self.assertFailure(
            checker.requestAvatarId(creds), UnauthorizedLogin)

    @inlineCallbacks
    def test_request_avatar(self):
        conn = yield self.connect_test_django_db()
        realm = GoggleServerRealm(conn, UploadResource)
        _, resource, _ = realm.requestAvatar('avatar-id', None, IResource)
        self.assertTrue(isinstance(resource, UploadResource))
