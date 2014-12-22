from zope.interface import implements

from twisted.application.service import IServiceMaker, Service
from twisted.cred import portal
from twisted.internet import reactor, endpoints
from twisted.plugin import IPlugin
from twisted.python import usage, log
from twisted.web.server import Site, Request
from twisted.web.guard import BasicCredentialFactory, HTTPAuthSessionWrapper

import psycopg2
import psycopg2.extras

from txpostgres import txpostgres

import dj_database_url

from goggles.server import resource
from goggles.server.auth import GoggleCredentialsChecker, GoggleServerRealm


DEFAULT_PORT = 'tcp:8080'
DEFAULT_DB_URL = 'postgres://localhost:5432/goggles'


def dict_connect(*args, **kwargs):
    kwargs['connection_factory'] = psycopg2.extras.DictConnection
    return psycopg2.connect(*args, **kwargs)


class DBConnection(txpostgres.Connection):
    connectionFactory = staticmethod(dict_connect)


class GoggleRequest(Request):
    # Place holder because I may need to process the chunks are they arrive
    pass


class GoggleService(Service):

    def __init__(self, options):
        self.options = options

    def startService(self):
        db_info = dj_database_url.parse(self.options['database-url'])
        conn = DBConnection()
        d = conn.connect('dbname=%(NAME)s' % db_info)
        d.addCallback(self.start_server)
        d.addErrback(self.stop_server)
        return d

    def stop_server(self, failure=None):
        if failure:
            log.err(failure)
        reactor.stop()

    def start_server(self, connection):
        checker = GoggleCredentialsChecker(connection)
        realm = GoggleServerRealm(connection, resource.GoggleResource)
        p = portal.Portal(realm, [checker])
        credentialFactory = BasicCredentialFactory("Goggles")
        protected_resource = HTTPAuthSessionWrapper(p, [credentialFactory])

        site = Site(protected_resource)
        site.requestFactory = GoggleRequest

        endpoint = endpoints.serverFromString(
            reactor, self.options['endpoint'])
        endpoint.listen(site)


class ServerOptions(usage.Options):
    """Command line args when run as a twistd plugin"""
    # TODO other args
    optParameters = [
        ["endpoint", "e", DEFAULT_PORT,
         "Endpoint for goggles server to listen on."],
        ["database-url", "d", DEFAULT_DB_URL,
         "The PostgreSQL database to connect to."]]


class GoggleServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "goggle-server"
    description = "The Goggle Server"
    options = ServerOptions

    def makeService(self, options):
        return GoggleService(options)
