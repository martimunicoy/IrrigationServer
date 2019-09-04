import os
from io import BytesIO
from http.server import CGIHTTPRequestHandler, _url_collapse_path

from routes import routes
from response.postKeys import post_keys
from response.htmlHandler import HTMLHandler
from response.staticHandler import StaticHandler
from response.cgiHandler import CGIHandler
from response.badRequestHandler import BadRequestHandler


class Server(CGIHTTPRequestHandler):
    cgi_directories = ['/server/response/cgi/']

    def do_HEAD(self):
        return

    """
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = str(self.rfile.read(content_length), 'utf-8')
        if (self.path == '/start'):
            print('Starting server')
            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()
        elif (self.path == '/send'):
            print('Sending')
            self.send_response(200)
            key, value = body.split('=')
        else:
            self.send_response(400)

        #
        #print(self.path)
        #print(body)

        #if (key in post_keys):
        #    self.send_response(200)
        #else:
        #    self.send_response(200)

        #from ast import literal_eval
        #python_dict = literal_eval(str(body, 'utf-8'))
        #print(python_dict)
        #self.send_response(200)
        #self.end_headers()
        #response = BytesIO()
        #response.write(b'This is POST request. ')
        #response.write(b'Received: ')
        #response.write(body)
        #self.wfile.write(response.getvalue())
        #
    """

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        print(split_path)

        if ((request_extension == '') or (request_extension == '.html')):
            if (self.path in routes):
                handler = HTMLHandler()
                handler.find(routes[self.path])
            else:
                handler = BadRequestHandler()

        elif (request_extension == '.py'):
            handler = BadRequestHandler()

        elif (request_extension == '.cgi'):
            collapsed_path = _url_collapse_path(self.path)
            dir_sep = collapsed_path.find('/', 1)
            self.cgi_info = (collapsed_path[:dir_sep],
                             collapsed_path[dir_sep + 1:])

            self.run_cgi()
            return

        else:
            handler = StaticHandler()
            handler.find(self.path)

        self._respond({'handler': handler})

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
