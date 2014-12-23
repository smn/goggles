# -*- test-case-name: goggles.server.tests.test_resource -*-
from twisted.web import http
from twisted.web.resource import Resource, NoResource
from twisted.web.server import NOT_DONE_YET


class BaseResource(Resource):

    def errback(self, failure, request):
        request.setResponseCode(http.INTERNAL_SERVER_ERROR)
        request.write(failure.getTraceback())
        request.finish()


class UserMessageResource(BaseResource):

    def __init__(self, job, direction):
        Resource.__init__(self)
        self.job = job
        self.direction = direction

    def render_POST(self, request):
        d = self.job.import_user_messages(
            self.direction, request.content, out=request)
        d.addCallback(lambda _: request.finish())
        d.addErrback(self.errback, request)
        return NOT_DONE_YET


class UploadResource(Resource):

    def __init__(self, job):
        Resource.__init__(self)
        self.inbound_resource = UserMessageResource(job, 'inbound')
        self.outbound_resource = UserMessageResource(job, 'outbound')

    def getChild(self, name, request):  # pragma: no cover
        return {
            'inbound': self.inbound_resource,
            'outbound': self.outbound_resource,
        }.get(name, NoResource())


class DownloadResource(Resource):

    def __init__(self, job):
        Resource.__init__(self)


class GoggleResource(Resource):

    def __init__(self, job):
        Resource.__init__(self)
        self.upload_resource = UploadResource(job)
        self.download_resource = DownloadResource(job)

    def getChild(self, name, request):  # pragma: no cover
        return {
            'upload': self.upload_resource,
            'download': self.download_resource,
        }.get(name, NoResource())
