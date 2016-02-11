from wsgiref.simple_server import make_server, demo_app

host = 'localhost'
port = 8080


class WebServer():

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self.response_value = (x for x in range(10))

    def __iter__(self):
        self.start('200 OK', [('Content-type', 'text/html')])
        value = next(self.response_value)
        print(value)
        yield str(value)


httpd = make_server(host, port, WebServer)

print('Serving HTTP on {}, port {}'.format(host, port))

httpd.serve_forever()
