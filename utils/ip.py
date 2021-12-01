import flask
import hashlib

def encode(ip: str):
    return hashlib.sha256(ip.encode()).hexdigest()

def get_raw(request: flask.Request):
    appengine_ip = request.headers.get("x-appengine-user-ip")
    if appengine_ip is None:
        return "0.0.0.0"

    return request.headers.get("x-appengine-user-ip")