from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class ImageAPIServer(BaseHTTPRequestHandler):

    def handle_images(self):
        self.send_response(200)

        self.send_header("Content-type", "application/json")
        self.end_headers()

        response_data = {"status": "success", "message": "Hello from Python!"}
        json_string = json.dumps(response_data)

        self.wfile.write(json_string.encode('utf-8'))

    def handle_image(self):
        ...

    def handle_upload(self):
        ...

    def do_GET(self):
        self.path = self.path.rstrip('/')

        if self.path == '/images':
            self.handle_images()
        elif self.path == '/images/':  # FIXME
            self.handle_image()

        def do_POST(self):
            if self.path == '/upload':
                self.handle_upload()


def run(server_class=HTTPServer, handler_class=ImageAPIServer, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
