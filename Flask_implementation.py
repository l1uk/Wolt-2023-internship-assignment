'''
Simple Flask APP with one GET endpoint. 
The only specified route is get-delivery-fee, and the parameters are separated by /. Leverages the Delivery class specified in the modules.
The parameters name are not provided in the url

When invoking the script, the port number is provided as an argument E.G.
python3 Stock-Flask_implementation.py 8000 

Example of a valid request: 

localhost:5000/get-delivery-fee/1/1500/1/2021-01-15T19:00:00Z
'''
from flask import Flask, jsonify, make_response, abort
from Classes.delivery import Delivery
import sys
app = Flask(__name__)

@app.route('/get-delivery-fee/<cart_value>/<delivery_distance>/<number_of_items>/<time>', methods=['GET'])
def calculateDeliveryFee(cart_value,delivery_distance,number_of_items,time):
    '''
    Try instatiating a Delivery object with the provided data and extracting the shipping fee attribute from it. 
    Finally, sets the headers and responds with the value. 
    ValueError(s) are thrown by the Delivery class in case the input is not validated, case in which the server will respond with a 400 code (bad request).  
    In case any other exception is thrown, the serer will reply with a 500 code (internal server error). 
    '''
    responseCode = 200
    response = None
    error = None
    try:
        deliveryObject = Delivery.retrieveFromCache(query_components = None,
                                   cart_value = cart_value, delivery_distance = delivery_distance, number_of_items = number_of_items, time = time)
        if deliveryObject == None:
            deliveryObject = Delivery(query_components = None,
                                    cart_value = cart_value, delivery_distance = delivery_distance, number_of_items = number_of_items, time = time)
        response = deliveryObject.getShippingFee()
    except ValueError as e:
        abort(400, str(e))
    except Exception as e:
        abort(500, "Generic server error " + str(e))
    response = make_response(
        jsonify({'delivery_fee': response}) if response != None else jsonify({'error': error}),
        200
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response

@app.errorhandler(404)
def not_found(e):
    """Page not found."""
    response = make_response(jsonify({'error': str(e)}), 404)
    response.headers['Content-Type'] = 'application/json'
    return response
@app.errorhandler(400)
def bad_request(e):
    """Invalid data provided."""
    response = make_response(jsonify({'error': str(e)}), 400)
    response.headers['Content-Type'] = 'application/json'
    return response
@app.errorhandler(500)
def server_fault(e):
    """Internal server error."""
    response = make_response(jsonify({'error': str(e)}), 500)
    response.headers['Content-Type'] = 'application/json'
    return response
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: %s <Port number>" %sys.argv[0])
        exit()
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Usage: %s <Port number>" %sys.argv[0])
        exit()       
    app.run(debug=False, port=port)