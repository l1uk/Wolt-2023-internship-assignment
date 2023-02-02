#!/usr/bin/env python3
"""An example HTTP server with GET and POST endpoints."""

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time
from urllib.parse import urlparse, parse_qs


# Sample blog post data similar to
# https://ordina-jworks.github.io/frontend/2019/03/04/vue-with-typescript.html#4-how-to-write-your-first-component
_g_posts = {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"}



class _RequestHandler(BaseHTTPRequestHandler):
    # Borrowing from https://gist.github.com/nitaku/10d0662536f37a087e1b
    associatedDelivery = None
    responseCode = HTTPStatus.OK.value
    errorMessage = None

    def _set_headers(self):
        self.send_response(self.getReponseStatus())
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self.checkRequest()
        self._set_headers()
        if(self.requestValidated):
            self.wfile.write(json.dumps(_g_posts).encode('utf-8'))
        else:
            self.wfile.write(self.getErrorMessage().encode('utf-8'))    

    def checkRequest(self):
        try:
            query_components = parse_qs(urlparse(self.path).query)
            cart_value = query_components["cart_value"]
            delivery_distance = query_components["delivery_distance"]
            number_of_items = query_components["number_of_items"]
            time = query_components["time"]
            print(cart_value)
        except KeyError:
            self.requestValidated = False
            return
        self.requestValidated = True
    
    def getErrorMessage(self):
        'todo'
        return"error"
    def getReponseStatus(self):
        if(self.associatedDelivery != None):
            return HTTPStatus.OK.value
        else:
            return HTTPStatus.BAD_REQUEST.value

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()