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
    raw_ip = request.remote_addr
    hashed_ip = ip.encode(raw_ip)

    if db.get_ip(hashed_ip) == None:
        db.add_ip(hashed_ip)
        return jsonify({"message": "200: success"})
    else:
        db.update_ip(hashed_ip)
        return jsonify({"message": "200: success"})


@app.route("/ip/check", methods=["GET"])
def ip_check():
    data = db.get_ip(ip.encode(request.remote_addr))

    can_send_req = timestamp.can_req(data)

    if can_send_req:
        return jsonify({"message": "200: success"})
    else:
        return jsonify({"message": "403: forbidden"})

@app.route("/dev/ip/get", methods=["GET"])
def dev_ip_get():
    token = request.headers.get("Authentication")

    if cnf.check_token(token):
        raw_ip = request.remote_addr
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
            return jsonify({"message": "404: not found"}), 404

    else:
        return jsonify({"message": "403: forbidden"})

@app.route("/dev/ip/delete", methods=["DELETE"])
def dev_ip_delete():
    token = request.headers.get("Authentication")

    if cnf.check_token(token):
        raw_ip = request.remote_addr
        hashed_ip = ip.encode(raw_ip)

        db.delete_ip(hashed_ip)

        return jsonify({"message": "200: success"})

    else:
        return jsonify({"message": "403: forbidden"})


if __name__ == "__main__":
   app.run()