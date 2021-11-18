from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="storage")
app.config["JSON_SORT_KEYS"] = False


from utils import ip, timestamp, config
from mysql_utils import database

db = database.MySQL()
cnf = config.Config()

@app.route("/")
def index():
    return "World Daily Mood API root, map at /map"

@app.route("/map")
def _map():
    return render_template("map.html")

@app.route("/ip/update", methods=["POST"])
def ip_update():
    raw_ip = request.headers.get("x-appengine-user-ip")
    hashed_ip = ip.encode(raw_ip)

    if db.get_ip(hashed_ip) == None:
        db.add_ip(hashed_ip)
    else:
        db.update_ip(hashed_ip)

    return jsonify({"message": "200: success"})


@app.route("/ip/check", methods=["GET"])
def ip_check():
    raw_ip = request.headers.get("x-appengine-user-ip")
    data = db.get_ip(ip.encode(raw_ip))

    can_send_req = timestamp.can_req(data)

    if can_send_req:
        return jsonify({"message": "200: success"})
    else:
        return jsonify({"message": "403: forbidden, you already sent a request today"}), 403


@app.route("/mood/add", methods=["POST"])
def mood_add():
    raw_ip = request.headers.get("x-appengine-user-ip")
    hashed_ip = ip.encode(raw_ip)
    mood = request.headers.get("Mood")
    data = db.get_ip(ip.encode(raw_ip))

    can_send_req = timestamp.can_req(data)

    if data == None:
        db.add_ip(hashed_ip)
        db.add_mood(hashed_ip, mood)

        return jsonify({"message": "200: success"})

    if can_send_req:
        db.add_mood(hashed_ip, mood)

        return jsonify({"message": "200: success"})

    else:
        return jsonify({"message": "403: forbidden, you already sent a request today"}), 403

@app.route("/mood/get", methods=["GET"])
def mood_get():
    raw_ip = request.headers.get("x-appengine-user-ip")
    mood = request.headers.get("Mood")

    mood = db.get_mood(ip.encode(raw_ip))

    if mood is not None:
        return jsonify({"mood": mood})
    else:
        return jsonify({"message": "404: IP record not found for today"}), 404


@app.route("/current/get", methods=["GET"])
def current_get():
    mood_data = db.get_current()

    if mood_data is not None:
        return jsonify({"mood": mood_data[0], "updated_at": mood_data[1]})
    else:
        return jsonify({"message": "404: No current mood"}), 404

@app.route("/dev/ip/get", methods=["GET"])
def dev_ip_get():
    token = request.headers.get("Authentication")

    if cnf.check_token(token):
        raw_ip = request.headers.get("target-ip")
        if raw_ip == None:
            raw_ip = request.headers.get("x-appengine-user-ip")

        hashed_ip = ip.encode(raw_ip)

        data = db.get_ip(hashed_ip)

        if data is not None:
            last_reqest, next_request, can_send_req = timestamp.get_all(data)

            return jsonify({"ip": {
                                "raw": raw_ip, 
                                "encoded": hashed_ip
                                }, 
                            "status": {
                                "last_request_at": last_reqest,
                                "next_request_at": next_request,
                                "send_request": can_send_req,
                            }

            }), 200

        else:
            return jsonify({"message": "404: IP address not found"}), 404

    else:
        return jsonify({"message": "403: forbidden, token invalid"}), 403

@app.route("/dev/ip/delete", methods=["DELETE"])
def dev_ip_delete():
    token = request.headers.get("Authentication")
    raw_ip = request.headers.get("target-ip")

    if cnf.check_token(token):
        if raw_ip == None:
            raw_ip = request.headers.get("x-appengine-user-ip")
        hashed_ip = ip.encode(raw_ip)

        db.delete_ip(hashed_ip)

        return jsonify({"message": "200: success"})

    else:
        return jsonify({"message": "403: forbidden, token invalid"}), 403


if __name__ == "__main__":
    from waitress import serve
    host = "0.0.0.0"
    port = 5000

    print(f"Running on {host}:{port}")
    serve(app, host="0.0.0.0", port=5000)