const express = require("express");
const fs = require("fs");
const { Keys } = require("./mysql/keys")

const app = express();
const port = 8080

let mysql_raw = fs.readFileSync("mysql/config.json");
let mysql_config = JSON.parse(mysql_raw);
const keys = new Keys(mysql_config["host"], mysql_config["username"], mysql_config["password"], mysql_config["database"]);

function check_api_key(req, res) {
    const api_key = req.get("Authentication");

    if (api_key == null) {
        res.status(401).send({"message": "401: Unauthorized"});
        return false;
    }
    
    keys.check(api_key)
}

app.get("/", (req, res) => {
    res.send("Api root");
});

app.get("/keycheck", (req, res) => {
    if (check_api_key(req, res) == false) {
        return;
    }

    res.send({data: "success"});
});

app.get("/test", (req, res) => {
    keys.test(keys)
});

app.listen(port, () => console.log("Server started on " + port));