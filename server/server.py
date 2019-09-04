import os
from io import BytesIO
from http.server import BaseHTTPRequestHandler

from routes import routes
from response.htmlHandler import HTMLHandler
from response.staticHandler import StaticHandler
from response.cgiHandler import CGIHandler
from response.badRequestHandler import BadRequestHandler


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')
        """
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if ((request_extension == '') or (request_extension == '.html')):
            if (self.path in routes):
                handler = HTMLHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()

        elif (request_extension == '.py'):
            handler = BadRequestHandler()

        elif (request_extension == '.cgi'):
            handler = CGIHandler()

        else:
            handler = StaticHandler()
            handler.find(self.path)

        self._respond({'handler': handler})
        """

    def _handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        if (status_code is 200):
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        if (isinstance(content, (bytes, bytearray))):
            return content

        return bytes(content, 'UTF-8')

    def _respond(self, opts):
        response = self._handle_http(opts['handler'])
        self.wfile.write(response)
