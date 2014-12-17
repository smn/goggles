from twisted.web.resource import Resource


class GoggleResource(Resource):

    debug = False
    isLeaf = True

    def __init__(self, conn):
        self.conn = conn

    def render_GET(self, request):
        return '%s %s' % (request.getUser(), self.conn)
