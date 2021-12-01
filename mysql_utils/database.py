import json
import mysql.connector
from utils import idgen

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

    # REQUESTS

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


    # REDIRECTS

    def create_redirect(self, mood: str):
        _id = idgen.generate()
        if self.get_redirect(_id) == None:
            connection = self.connect()
            cursor = connection.cursor()

            query = "INSERT INTO redirects (id, mood) VALUES (%s, %s)"
            cursor.execute(query, (_id, mood,))

            connection.commit()
            connection.close()

            return _id

        return self.create_redirect(mood)

    def get_redirect(self, id: str):
        connection = self.connect()
        cursor = connection.cursor()

        query = "SELECT * FROM redirects WHERE id = %s"
        cursor.execute(query, (id,))

        result = cursor.fetchone()
        connection.close()

        return result