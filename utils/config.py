import hashlib
import json

config_file = "./storage/config.json"

class Config:
    def __init__(self):
        try:
            with open(config_file, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("Main config file (./storage/config.json) is missing")
            exit(1)

    def check_token(self, token):
        if token is not None:
            if hashlib.sha256(token.encode()).hexdigest() == self.get_admin_token():
                return True

    def get_admin_token(self):
        return self.config["admin_token"]

    def get_valid_moods(self):
        return self.config["moods"]

    def get_configfiles(self):
        return self.config["configfiles"]