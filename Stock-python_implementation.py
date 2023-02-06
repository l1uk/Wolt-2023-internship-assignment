'''
Simple HTTP server with one GET endpoint. Implemented by overriding the BaseHTTPRequestHandler class used by the HTTPServer class to reply to requests 
and serve files normally.
 
When invoking the script, the port number is provided as an argument E.G.
python3 Stock-python_implementation.py 8000 

Examples of valid requests (See classes.RequestHandler docs for further info):

localhost:8000/getFee?cart_value=999&delivery_distance=10&number_of_items=1&time=2021-01-14T19:00:00Z ;

localhost:8000/getDeliveryFee?cart_value=999&delivery_distance=10&number_of_items=1&time=2021-01-14T19:00:00Z ;

localhost:8000/?cart_value=999&delivery_distance=10&number_of_items=1&time=2021-01-14T19:00:00Z ;

localhost:8000?cart_value=999&delivery_distance=10&number_of_items=1&time=2021-01-14T19:00:00Z.
'''

from http.server import HTTPServer
from Classes.RequestHandler import _RequestHandler
import sys
def run_server(port):
    '''
    Simple method that instantiates the HTTPServer Object with the custom RequestHandler class and start it.
    '''
    server_address = ('', port)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: %s <Port number>" %sys.argv[0])
        exit()
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Usage: %s <Port number>" %sys.argv[0])
        exit()       
    run_server(port)