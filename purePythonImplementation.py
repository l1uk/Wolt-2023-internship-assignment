#!flask/bin/python3
'''
Simple HTTP server with one GET endpoint. Implemented by overriding the BaseHTTPRequestHandler class used by the HTTPServer class to reply to requests 
and serve files normally. The parameters in the URL are delimited by an initial ? and specified in standard GET notation (<Name>=<Value>) separated by &.
Since we have one single endpoint, only the query parameters of the request are checked and not the endpoint. Leverages the Delivery class specified in the modules.

For instance, these are all valid requests:
localhost:8000/getFee?cart_value=999&delivery_distance=10&number_of_items=1&time=2021-01-14T19:00:00Z ;
localhost:8000/getDeliveryFee?cart_value=999&delivery_distance=10&number_of_items=1&time=2021-01-14T19:00:00Z ;
localhost:8000/?cart_value=999&delivery_distance=10&number_of_items=1&time=2021-01-14T19:00:00Z ;
localhost:8000?cart_value=999&delivery_distance=10&number_of_items=1&time=2021-01-14T19:00:00Z.
'''

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time
from urllib.parse import urlparse, parse_qs
from module.delivery import Delivery



class _RequestHandler(BaseHTTPRequestHandler):
    # Inspired from https://gist.github.com/nitaku/10d0662536f37a087e1b
    associatedDeliveryObject = None
    responseCode = HTTPStatus.OK.value
    errorMessage = {"error": "Generic error"}
    responseValue = None

    def _set_headers(self):
        '''
        Simple method to set header for the response. 
        The content type is set as JSON and requests are allowed from any origin to enable local development.  
        '''
        self.send_response(self.responseCode)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        '''
        Parses the request parameters into a dictionary using the parse_qs method from urllib, 
        and try instatiating a Delivery object with the parsed data and extracting the shipping fee attribute from it. 
        ValueError(s) are thrown by the Delivery class in case the input is not validated, case in which the server will respond with a 400 code (bad request).  
        In case any other exception is thrown, the serer will reply with a 500 code (internal server error). 
        Finally, the response headers are set (depending on the outcome of the validation) and a response is sent to the client. 
        '''
        requestParams = parse_qs(urlparse(self.path).query)
        try:
            self.associatedDeliveryObject = Delivery(query_components = requestParams)
            self.responseValue = {"delivery_fee": self.associatedDeliveryObject.getShippingFee()}
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
    '''
    Simple method that instantiates the HTTPServer Object with the custom RequestHandler class and start it.
    '''
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()