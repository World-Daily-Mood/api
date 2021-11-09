const { createHash } = require("crypto");
const { randomBytes } = require("crypto");

function generate() {
    return createHash("sha256").update(randomBytes(16).toString("hex")).digest("hex");
}

function hash(key){
    return createHash('sha256').update(key).digest('hex');
}

function check(req, res, mysql) {
    const api_key = req.get("Authentication");

    return new Promise((resolve, reject) => {
        function check_presence(key) {
            if (key == null) {
                res.status(403).send({"message": "403: Forbidden"});
                return false
            } else {
                return true
            }
        }

        function check_format(key) {
            if (key.length != 32) {
                res.status(403).send({"message": "403: Forbidden"});
                return false;
            } else {
                return true
            }
        }

        function check_db(key){
            return new Promise((resolve, reject) => {
                mysql.key_check(hash(api_key)).then(function(result){
                    if (result != true) {
                        res.status(403).send({"message": "403: Forbidden"});
                        resolve(false);
                    } else {
                        resolve(true)
                    }
                });
            });
        }
        
        if (check_presence(api_key) && check_format(api_key)) {
                check_db(api_key).then(function(result){
                    resolve(result);
                });
        }
    });
}


module.exports = {
    check: check,
}