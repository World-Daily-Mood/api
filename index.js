const express = require("express");
const fs = require("fs");
const key = require("./utils/key")
const { createHash } = require('crypto');
const { Mysql } = require("./mysql/mysql");

const app = express();
const port = 8080

let mysql_raw = fs.readFileSync("mysql/config.json");
let mysql_config = JSON.parse(mysql_raw);
const mysql = new Mysql(mysql_config["host"], mysql_config["username"], mysql_config["password"], mysql_config["database"]);

app.get("/", (req, res) => {
    res.send("Api root");
});

app.get("/key/check", (req, res) => {
    key.check(req, res, mysql).then(function(result){
        if (result == true) {
            res.send({message: "200: OK"})
        }
    });
});

app.get("/user/register", (req, res) => {
    const hashed_email = createHash("sha256").update(req.get("Email")).digest("hex");
    const hashed_password = createHash("sha256").update(req.get("Password")).digest("hex");

    const user_id =  Math.floor(Math.random() * (9999999999 - 1000000000) + 1000000000);

    mysql.user_add(user_id, hashed_email, hashed_password).then(result => {
    res.send({"email": email, "password": password, "user_id": user_id});
    });
});

app.listen(port, () => console.log("Server started on " + port));