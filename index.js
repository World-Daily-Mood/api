const express = require("express");
const fs = require("fs");
const { Keys } = require("./mysql/keys")

const app = express();
const port = 8080

let mysql_raw = fs.readFileSync("mysql/config.json");
let mysql_config = JSON.parse(mysql_raw);
const keys = new Keys(mysql_config["host"], mysql_config["username"], mysql_config["password"], mysql_config["database"]);

function check_key_presence(req, res) {
    const api_key = req.get("Authentication");

    if (api_key == null) {
        res.status(403).send({"message": "403: Forbidden"});
        return false
    } else {
        return true;
    }
}

function api_key_is_valid(req, res) {
    const api_key = req.get("Authentication");

    if (check_key_presence(req, res)) {
        return new Promise(function(resolve, reject) {
            keys.check(api_key).then(result => {
                if (result) {
                    resolve(result);
                } else {
                    res.status(403).send({"message": "403: Forbidden"});
                    resolve(result);
                }
            });
        }
    )} else {
        return new Promise(function(resolve, reject) {
            resolve(false);
        }); 
    }
}

app.get("/", (req, res) => {
    res.send("Api root");
});

app.get("/key/check", (req, res) => {
    const api_key = req.get("Authentication");

    api_key_is_valid(req, res).then(result => {
        if (result) {
            res.send({data: api_key});
        }
    });
});



/*
    if (check_key_presence(req, res) == true) {
        keys.check(api_key, function(err, result) {
        if (result == true) {
            res.send({data: api_key});

        } else {
            res.status(403).send({"message": "403: Forbidden"});
        }
        });
    }


});
*/

app.get("/key/generate", (req, res) => {
    var api_keys = keys.generate(2);
    console.log(api_keys);

    res.send(api_keys);
});

//console.log(app._router.stack);

app.listen(port, () => console.log("Server started on " + port));