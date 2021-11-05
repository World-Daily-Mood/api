const mysql = require("mysql");

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

    disconnect(connection){
        connection.end()
    }

    check(key){
        var connection = this.connect()

        var query = connection.query(`SELECT user_id from api_keys where api_key = '${key}';`, function(err, result){
            if(err) throw err;
            
            console.log(result[0]["user_id"]);

        });

        this.disconnect(connection)

    }
}

module.exports.Keys = Keys;