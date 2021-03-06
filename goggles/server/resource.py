# -*- test-case-name: goggles.server.tests.test_resource -*-
from twisted.internet.defer import inlineCallbacks
from twisted.web import http
from twisted.web.resource import Resource, NoResource
from twisted.web.server import NOT_DONE_YET

import treq


class BaseResource(Resource):

    def errback(self, failure, request):
        request.setResponseCode(http.INTERNAL_SERVER_ERROR)
        request.write(failure.getErrorMessage())


class UploadUserMessageResource(BaseResource):

    def __init__(self, job_helper, direction):
        Resource.__init__(self)
        self.job_helper = job_helper
        self.direction = direction

    def render_POST(self, request):
        d = self.job_helper.import_user_messages(
            self.direction, request.content, out=request)
        d.addErrback(self.errback, request)
        d.addBoth(lambda *a: request.finish())
        return NOT_DONE_YET


class UploadResource(Resource):

    def __init__(self, job_helper):
        Resource.__init__(self)
        self.inbound_resource = UploadUserMessageResource(
            job_helper, 'inbound')
        self.outbound_resource = UploadUserMessageResource(
            job_helper, 'outbound')

    def getChild(self, name, request):  # pragma: no cover
        return {
            'inbound': self.inbound_resource,
            'outbound': self.outbound_resource,
        }.get(name, NoResource())


class DownloadUserMessageResource(BaseResource):

    def __init__(self, job_helper, direction):
        Resource.__init__(self)
        self.job_helper = job_helper
        self.direction = direction

    @inlineCallbacks
    def download_conversation(self, request, import_job):
        profile = yield self.job_helper.fetch_profile()
        conversation = yield self.job_helper.fetch_conversation(
            import_job['conversation_id'])
        url = ('https://go.vumi.org/conversations/%s/export_messages/'
               '?direction=%s&format=json')
        response = yield treq.get(
            url % (conversation['conversation_key'], self.direction),
            cookies={
                profile['session_name']: profile['session_value'],
            })

        d = treq.collect(
            response,
            self.job_helper.import_user_messages_chunk(
                self.direction, request))
        d.addBoth(lambda *a: request.finish())
        yield d

    def render_GET(self, request):
        def cb(job):
            if job is None:
                request.setResponseCode(http.NOT_FOUND)
                request.finish()
                return

            d = self.download_conversation(request, job)
            d.addErrback(self.errback, request)
            return d

        d = self.job_helper.fetch_job()
        d.addCallback(cb)
        d.addBoth(lambda *a: request.finish())
        return NOT_DONE_YET


class DownloadResource(Resource):

    def __init__(self, job_helper):
        Resource.__init__(self)
        self.inbound_resource = DownloadUserMessageResource(
            job_helper, 'inbound')
        self.outbound_resource = DownloadUserMessageResource(
            job_helper, 'outbound')

    def getChild(self, name, request):  # pragma: no cover
        return {
            'inbound': self.inbound_resource,
            'outbound': self.outbound_resource,
        }.get(name, NoResource())


class GoggleResource(Resource):

    def __init__(self, job_helper):
        Resource.__init__(self)
        self.upload_resource = UploadResource(job_helper)
        self.download_resource = DownloadResource(job_helper)

    def getChild(self, name, request):  # pragma: no cover
        return {
            'upload': self.upload_resource,
            'download': self.download_resource,
        }.get(name, NoResource())
