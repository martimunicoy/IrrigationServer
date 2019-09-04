import os
from response.requestHandler import RequestHandler


class StaticHandler(RequestHandler):
    def __init__(self):
        self.__filetypes = {
            ".js": "text/javascript",
            ".css": "text/css",
            ".jpg": "image/jpeg",
            ".png": "image/png",
            "notfound": "text/plain"
        }

    def find(self, file_path):
        split_path = os.path.splitext(file_path)
        extension = split_path[1]

        path = os.path.join(os.path.dirname(__file__),
                            'static', *file_path.split('/'))
        print(path)

        try:
            if (extension in (".jpg", ".jpeg", ".png")):
                self.contents = open(path, 'rb')
            else:
                self.contents = open(path, 'r')
            self.setContentType(extension)
            self.setStatus(200)
            return True

        except (FileNotFoundError, IsADirectoryError):
            self.setContentType('notfound')
            self.setStatus(404)
            return False

    def setContentType(self, ext):
        self.contentType = self.__filetypes[ext]
