#!/usr/bin/env python3
""" Simple HTTP server with one GET endpoint."""

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time
from urllib.parse import urlparse, parse_qs
from module.delivery import Delivery



class _RequestHandler(BaseHTTPRequestHandler):
    # Inspired from https://gist.github.com/nitaku/10d0662536f37a087e1b
    associatedDelivery = None
    responseCode = HTTPStatus.OK.value
    # possibilmente includere l'errore nell'oggetto
    errorMessage = {"error": "Generic error"}
    responseValue = None

    def _set_headers(self):
        self.send_response(self.responseCode)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self): 
        requestParams = parse_qs(urlparse(self.path).query)
        try:
            self.associatedDelivery = Delivery(requestParams)
            self.responseValue = {"delivery_fee": self.associatedDelivery.getShippingFee()}
        except ValueError as e:
            self.responseValue = None
            self.responseCode = HTTPStatus.BAD_REQUEST.value
            self.errorMessage = {"error": str(e)}
        except:
            self.responseValue = None
            self.responseCode = HTTPStatus.INTERNAL_SERVER_ERROR.value
        self._set_headers()
        if(self.responseValue != None):
            self.wfile.write(json.dumps(self.responseValue).encode('utf-8'))
        else:
            self.wfile.write(json.dumps(self.errorMessage).encode('utf-8'))    



def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()