import json
import mysql.connector

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

    def get_ip(self, hashed_ip):
        connection = self.connect()
        cursor = connection.cursor()

        query = "SELECT * FROM requests WHERE ip = %s"
        cursor.execute(query, (hashed_ip,))

        result = cursor.fetchone()
        connection.close()

        return result

    def add_ip(self, hashed_ip):
        connection = self.connect()
        cursor = connection.cursor()

        query = "INSERT INTO requests (ip) VALUES (%s)"
        cursor.execute(query, (hashed_ip,))

        connection.commit()
        connection.close()

    def delete_ip(self, hashed_ip):
        connection = self.connect()
        cursor = connection.cursor()

        query = "DELETE FROM requests WHERE ip = %s"
        cursor.execute(query, (hashed_ip,))

        connection.commit()
        connection.close()
        
    def update_ip(self, hashed_ip):
        connection = self.connect()
        cursor = connection.cursor()

        query = "UPDATE requests SET date = current_timestamp() WHERE ip = %s"
        cursor.execute(query, (hashed_ip,))

        connection.commit()
        connection.close()


    def add_mood(self, hashed_ip, mood):
        connection = self.connect()
        cursor = connection.cursor()

        query = "INSERT INTO today (ip, mood) VALUES (%s, %s)"
        cursor.execute(query, (hashed_ip, mood))

        connection.commit()
        connection.close()

    def get_mood(self, hashed_ip):
        connection = self.connect()
        cursor = connection.cursor()

        query = "SELECT mood FROM today WHERE ip = %s"
        cursor.execute(query, (hashed_ip,))

        result = cursor.fetchone()
        connection.close()

        if result is not None:
            return result[0]
        else:
            return None