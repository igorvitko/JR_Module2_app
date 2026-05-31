from http.server import BaseHTTPRequestHandler
import json

from utils import AppJSONEncoder


class BaseHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        json_string = json.dumps(data, cls=AppJSONEncoder)
        self.wfile.write(json_string.encode('utf-8'))

    def _send_error(self, status_code: int, message: str):
        self._send_json(status_code, {"error": message})

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
