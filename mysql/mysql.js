const mysql = require("mysql");
const { createHash } = require('crypto');
const { randomBytes } = require("crypto");

class Mysql {
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

    key_check(hashed_key) {
        const connection = this.connect();

        return new Promise(function(resolve, reject) {
            connection.query("SELECT user_id FROM api_keys WHERE api_key = ?", [hashed_key], function(err, rows) {

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


    key_generate(user_id) {
        const key = randomBytes(16).toString("hex");
        const hashed_key = createHash("sha256").update(key).digest("hex");
      
        var connection = this.connect()

        this.key_check(hashed_key).then(function(result) {
            if (result == false) {
                connection.query("INSERT INTO api_keys (user_id, api_key) VALUES (?, ?)", [user_id, hashed_key], function(err, rows) {
                    if (err) throw err;
                });
            }
        });

        return key;
    }

    user_is_registered(hashed_email) {
        const connection = this.connect();

        return new Promise(function(resolve, reject) {
            connection.query("SELECT user_id FROM users WHERE email = ?", [hashed_email], function(err, rows) {
                if (err) throw err;
                if (rows.length > 0) {
                    resolve(true);
                } else {
                    resolve(false);
                }
            });
        });
    }

    user_add(user_id, hashed_email, hashed_password) {
        var connection = this.connect();

        this.user_is_registered(hashed_email).then(function(result) {
            if (result == false) {

                return new Promise(function(resolve, reject) {

                    connection.query("INSERT INTO users (user_id, email, password) VALUES (?, ?, ?)", [user_id, hashed_email, hashed_password], function(err, rows) {
                    if (err) throw err;
                    resolve(true);

                    });
                });
            }
        });
    }
}

module.exports.Mysql = Mysql;