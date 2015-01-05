# -*- test-case-name: goggles.server.tests.test_auth -*-
from zope.interface import implements

from twisted.cred import portal, checkers, credentials, error
from twisted.web.resource import IResource
from twisted.internet.defer import inlineCallbacks, returnValue

from goggles.helper import ImportJobHelper


class GoggleCredentialsChecker(object):
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def __init__(self, conn):
        self.conn = conn

    @inlineCallbacks
    def requestAvatarId(self, credentials):
        result = yield self.conn.runQuery("""
            SELECT id FROM warehouse_importjob
            WHERE username_token = %s
            AND password_token = %s
            """, (credentials.username, credentials.password))
        try:
            [match] = result
            returnValue(match['id'])
        except ValueError:
            raise error.UnauthorizedLogin('Invalid access tokens')


class GoggleServerRealm(object):
    implements(portal.IRealm)

    def __init__(self, conn, resource_class):
        self.conn = conn
        self.resource_class = resource_class

    def requestAvatar(self, avatar_id, mind, *interfaces):
        if IResource in interfaces:
            return (IResource,
                    self.resource_class(
                        ImportJobHelper(self.conn, avatar_id)),
                    lambda: None)
        raise NotImplementedError()  # pragma: no cover
