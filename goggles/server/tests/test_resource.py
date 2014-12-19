from goggles.server.tests.base import GoggleTestCase
from goggles.server.resource import GoggleResource
from goggles.service import GoggleServerRealm
from goggles.server.auth import GoggleCredentialsChecker

from twisted.cred import portal
from twisted.internet.defer import inlineCallbacks
from twisted.web.guard import BasicCredentialFactory, HTTPAuthSessionWrapper


class TestGoggleResource(GoggleTestCase):

    @inlineCallbacks
    def setUp(self):
        self.conn = yield self.connect_test_db()
        self.resource = GoggleResource(self.conn)

    def test_authenticated_resource(self):
        checker = GoggleCredentialsChecker(self.conn)
        realm = GoggleServerRealm(self.resource)
        p = portal.Portal(realm, [checker])
        credentialFactory = BasicCredentialFactory("Goggles")
        protected_resource = HTTPAuthSessionWrapper(p, [credentialFactory])
        req = self.make_request()
        protected_resource.render(req)
        self.assertEqual(
            req.responseHeaders.getRawHeaders('www-authenticate'),
            ['basic realm="Goggles"'])

    def test_resource(self):
        req = self.make_request()
        print self.resource.render_GET(req)
