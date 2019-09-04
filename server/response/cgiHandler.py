from http.server import CGIHTTPRequestHandler

from .requestHandler import MockFile


class CGIHandler(CGIHTTPRequestHandler):
    def __init__(self):
        self.contentType = ""
        self.__cgi_directories = ["/cgi"]
        self.setStatus(200)
        self.contents = MockFile()

    def getContents(self):
        return self.contents.read()

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def getContentType(self):
        return self.contentType

    def getType(self):
        return 'static'
