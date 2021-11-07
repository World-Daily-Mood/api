const mysql = require("mysql");
const { createHash } = require('crypto');
const { randomBytes } = require("crypto");

class Keys {
    constructor(host, user, password, database) {
        this.host = host;
        this.user = user;
        this.password = password;
        this.database = database;
    }

    connect() {
        return mysql.createConnection({
            host: this.host,
            user: this.user,
            password: this.password,
            database: this.database
        });
    }

    check(key) {
        const connection = this.connect();
        const api_key = createHash('sha256').update(key).digest('hex');

        return new Promise(function(resolve, reject) {
            connection.query("SELECT user_id FROM api_keys WHERE api_key = ?", [api_key], function(err, rows) {

                if (err) throw err;
                if (rows.length > 0) {
                    resolve(true);
                }
                else {
                    resolve(false);
                }

            });

            connection.end();
        });
    }


    generate(user_id) {
        const key = randomBytes(16).toString("hex");
        const hashed_key = createHash("sha256").update(key).digest("hex");
      
        var connection = this.connect()
        connection.query(`SELECT api_key from api_keys where api_key = '${key}';`, function(err, result){
            if(err) throw err;

            if (result == null){
                generate();
            }
            else{
                connection.query(`INSERT INTO api_keys (user_id, api_key) VALUES (${user_id}, "${hashed_key}");`, function(err, result){
                    if(err) throw err;
                });
            }
        });

        connection.end();
        return {key, hashed_key};
    }
}

module.exports.Keys = Keys;