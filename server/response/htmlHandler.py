import os
from response.requestHandler import RequestHandler


class HTMLHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = 'text/html'

    def find(self, routeData):
        try:
            path = os.path.join(os.path.dirname(__file__),
                                'html', routeData['template'])
            template_file = open(path)
            self.contents = template_file
            self.setStatus(200)
            return True

        except (FileNotFoundError, IsADirectoryError):
            self.setStatus(404)
            return False
