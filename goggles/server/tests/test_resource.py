from goggles.server.tests.base import GoggleTestCase
from goggles.server.resource import GoggleResource

from twisted.internet.defer import inlineCallbacks
from twisted.web.test.test_web import DummyRequest


class TestGoggleResource(GoggleTestCase):

    @inlineCallbacks
    def setUp(self):
        conn = yield self.connect_test_db()
        self.resource = GoggleResource(conn)

    def test_resource(self):
        print self.resource
