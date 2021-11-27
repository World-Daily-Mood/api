from flask import jsonify
from flask.helpers import make_response

def send(content, status_code=200):
    response = make_response(jsonify(content), status_code)
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response