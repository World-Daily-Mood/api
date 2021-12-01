import flask
import hashlib

def encode(ip: str):
    return hashlib.sha256(ip.encode()).hexdigest()

def get_raw(request: flask.Request, support_custom: bool = False):
    appengine_ip = request.headers.get("x-appengine-user-ip")
    if support_custom == False:
        if appengine_ip is None:
            return "0.0.0.0"

    else:
        
        if appengine_ip is None:
            if request.headers.get("ip") is None:
                return "0.0.0.0"

            else:
                return request.headers.get("ip")
        else:
            return appengine_ip


    return request.headers.get("x-appengine-user-ip")