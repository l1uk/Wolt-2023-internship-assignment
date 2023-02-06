'''
Custom RequestHandler class (Parent Class: BaseHTTPRequestHandler), used for replying to HTTP request according to the desidered logic.

In particular, the do_GET method is overrided to parse the request parameters and create a Delivery object, which attributes will be used for the response. 
The parameters in the URL are delimited by an initial ? and specified in standard GET notation (<Name>=<Value>) separated by &.


Since there's one single endpoint for this case, only the query parameters of the request are checked and not the endpoint. 
Leverages the Delivery class specified in the modules.
'''
from http.server import BaseHTTPRequestHandler
from http import HTTPStatus
import json
from urllib.parse import urlparse, parse_qs
from Classes.delivery import Delivery

class _RequestHandler(BaseHTTPRequestHandler):
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
