import os
from http.server import CGIHTTPRequestHandler

from .requestHandler import MockFile


class CGIHandler(CGIHTTPRequestHandler):
    cgi_directories = ['/server/response/cgi/']

    def __init__(self, path, *args, **kwargs):
        self.path = path
        super().__init__(*args, **kwargs)
        self.setStatus(200)
        self.contents = MockFile()
        self.headers = []

    def getContents(self):
        return self.contents.read()

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def getContentType(self):
        return self.contentType

    def getType(self):
        return 'cgi'

    def find(self, file_path):
        print(file_path.split('/'))
        try:
            path = os.path.join(os.path.dirname(__file__),
                                self.__cgi_directory,
                                *file_path.split('/'))
            cgi_file = open(path)
            self.contents = cgi_file
            self.setStatus(200)
            return True

        except (FileNotFoundError, IsADirectoryError):
            self.setStatus(404)
            return False


