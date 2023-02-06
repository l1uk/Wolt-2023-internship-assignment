# HTTP API for Delivery Fee Calculation


This Python project is presented as a solution to [Wolt Summer 2023 Engineering Internships](https://github.com/woltapp/engineering-summer-intern-2023) backend assignment.

It provides a single endpoint HTTP API capable of serving a delivery fee with a basic caching mechanism. The API only support the GET method.


Two different solutions are implemented: the first one makes use of the Flask framework, while the second one is implemented using just stock Python. 
For more detailed information, please refer to the [project documentation](https://l1uk.github.io).

Note: [the official github repository](https://github.com/l1uk/Python-HTTP-api-for-delivery-fee-calculation) for the project will be made public on Tuesday, Feb 7th.

## Setup

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the project's dependencies.

```python
pip3 install -r requirements.txt
```

## Startup

To start the server invoke the script, specifying the port number as a command-line argument.
```python

# starts the Flask API at port 5000
python3 Flask_implementation.py 5000

# starts the Stock Python implementation at port 8000
python3 Stock-python_implementation.py 8000

```
## Usage
Sample requests with the corresponding responses are shown here.
```console
$ wget -q -O - "localhost:5000/get-delivery-fee/1/1500/1/2021-01-15T19:00:00Z"
{"delivery_fee":1500}

$ wget -q -O - "localhost:8000/getFee?cart_value=1000&delivery_distance=1500&number_of_items=12&time=2021-01-14T19:00:00Z"
{"delivery_fee": 700}
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
