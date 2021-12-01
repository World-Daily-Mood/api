import json
import mysql.connector
from mysql.connector.fabric import connection

configfile = "./mysql_utils/config.json"

class MySQL:
    def __init__(self):
        with open(configfile) as f:
            config = json.load(f)

        self.host = config["host"]
        self.user = config["user"]
        self.password = config["password"]
        self.database = config["database"]

    def connect(self):
        return mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )

    def add_request(self, hashed_ip: str, mood: str):
        connection = self.connect()
        cursor = connection.cursor()

        query = "INSERT INTO requests (ip, mood) VALUES (%s, %s)"
        cursor.execute(query, (hashed_ip, mood,))

        connection.commit()
        connection.close()

    def get_request(self, hashed_ip: str):
        connection = self.connect()
        cursor = connection.cursor()

        query = "SELECT * FROM requests WHERE ip = %s ORDER BY updated_at DESC LIMIT 1"
        cursor.execute(query, (hashed_ip,))

        result = cursor.fetchone()
        connection.close()

        return result

    def delete_requests(self, hashed_ip):
        connection = self.connect()
        cursor = connection.cursor()

        query = "DELETE FROM requests WHERE ip = %s"
        cursor.execute(query, (hashed_ip,))

        connection.commit()
        connection.close()