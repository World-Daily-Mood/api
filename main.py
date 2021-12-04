from flask import Flask, request, jsonify

app = Flask(__name__, template_folder="storage", static_folder=None)
app.config["JSON_SORT_KEYS"] = False

from utils import ip, timestamp, config, send_res, mood_check, idgen
from mysql_utils import database

db = database.MySQL()
cnf = config.Config()

base_url = "https://world-mood-333716.appspot.com"

@app.route("/")
def index():
    return "World Daily Mood API root, map at /map"

@app.route("/map")
def url_map():
    url_map = {}

    for rule in app.url_map.iter_rules():

        endpoint_methods = "["
        for method in rule.methods:
            endpoint_methods += method + ", "
        endpoint_methods = endpoint_methods[:-2] + "]"
        
        required = None
        if "dev" in rule.rule:
            required = "Authentication: token, (valid dev token)"
        

        url_description = {"endpoint": rule.rule, "methods": endpoint_methods, "required_headers": required}

        url_map[rule.rule] = url_description

    return jsonify(url_map)


@app.route("/ip/check", methods=["GET"])
def ip_check():
    raw_ip = ip.get_raw(request)
    data = db.get_request(ip.encode(raw_ip))

    can_send_req = timestamp.can_req(data)

    if can_send_req:
        return send_res.send({"message": "200: success"})
    else:
        return send_res.send({"message": "403: forbidden, you already sent a request today"}, 403)

@app.route("/mood/add", methods=["POST"])
def mood_add():
    raw_ip = ip.get_raw(request)
    hashed_ip = ip.encode(raw_ip)
    mood = request.headers.get("mood")

    if mood is not None:
        data = db.get_request(hashed_ip)

        if data is None:
            db.add_request(hashed_ip, mood)
            return send_res.send({"message": "200: success"})
        
        else:
            can_send_req = timestamp.can_req(data[0])

            if can_send_req:
                db.add_request(hashed_ip, mood)

                return send_res.send({"message": "200: success"})
        
            else:
                return send_res.send({"message": "403: forbidden, you already sent a request today"}, 403)
    
    else:
        return send_res.send({"message": "400: bad request, no mood specified"}, 400)


@app.route("/mood/get", methods=["GET"])
def mood_get():
    raw_ip = ip.get_raw(request)

    data = db.get_request(ip.encode(raw_ip))

    if data is not None:
        if timestamp.can_req(data) == False:
            return send_res.send({"mood": data[1]})

        else:
            return send_res.send({"message": "404: IP record not found for the last 24 hours"}, 404)

    else:
        return send_res.send({"message": "404: not found, no requests found for this ip"}, 404)

@app.route("/mood/is-valid", methods=["GET"])
def mood_is_valid():
    mood = request.args.get("mood")

    if mood is not None:
        if mood_check.is_valid(mood):
            return send_res.send({"message": "200: success"})
        else:
            return send_res.send({"message": "400: bad request, invalid mood"}, 400)
    else:
        return send_res.send({"message": "400: bad request, no mood specified"}, 400)
        
@app.route("/mood-bot", methods=["GET"])
def mood_bot():
    mood = request.args.get("mood")
    raw_ip = ip.get_raw(request)
    hashed_ip = ip.encode(raw_ip)

    if mood_check.is_valid(mood):
        data = db.get_request(hashed_ip)
        
        if timestamp.can_req(data):
            db.add_request(hashed_ip, mood)
            return send_res.send({"message": "200: success"})

        else:
            return send_res.send({"message": "403: forbidden, you already sent a request today"}, 403)
    else:
        return send_res.send({"message": "400: bad request, invalid mood"}, 400)

@app.route("/current/get", methods=["GET"])
def current_get():
    data = db.get_current()

    if data is not None:
        return send_res.send({"mood": data[0], "updated_at": data[1]})
    else:
        return send_res.send({"message": "404: No current mood"}, 404)

@app.route("/dev/ip/get", methods=["GET"])
def dev_ip_get():
    token = request.headers.get("Authentication")

    if cnf.check_token(token):
        raw_ip = ip.get_raw(request)
        if raw_ip == None:
            raw_ip = request.headers.get("x-appengine-user-ip")

        hashed_ip = ip.encode(raw_ip)

        data = db.get_request(hashed_ip)

        if data is not None:
            last_reqest, next_request, can_send_req = timestamp.get_all(data)

            return send_res.send({"ip": {
                                "raw": raw_ip, 
                                "encoded": hashed_ip
                                }, 
                            "status": {
                                "last_request_at": last_reqest,
                                "next_request_at": next_request,
                                "send_request": can_send_req,
                            },
                            "last_mood": data[1]

            })

        else:
            return send_res.send({"message": "404: IP address not found"}, 404)

    else:
        return send_res.send({"message": "403: forbidden, token invalid"}, 403)

@app.route("/dev/ip/delete", methods=["DELETE"])
def dev_ip_delete():
    token = request.headers.get("Authentication")

    if cnf.check_token(token):
        raw_ip = ip.get_raw(request)
        hashed_ip = ip.encode(raw_ip)
        ip_data = db.get_request(hashed_ip)

        if ip_data is not None:
            db.delete_requests(hashed_ip)
            return send_res.send({"message": "200: success"})

        else:
            return send_res.send({"message": "404: IP address not found"}, 404)

    else:
        return send_res.send({"message": "403: forbidden, token invalid"}, 403)


if __name__ == "__main__":
    from waitress import serve
    host = "0.0.0.0"
    port = 5000

    print(f"Running on {host}:{port}")
    serve(app, host="0.0.0.0", port=5000)