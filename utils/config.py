import hashlib
import json

config_file = "./storage/config.json"

class Config:
    def __init__(self):
        with open(config_file, "r") as f:
            self.config = json.load(f)  

    def check_token(self, token):
        if token is not None:
            if hashlib.sha256(token.encode()).hexdigest() == self.get_admin_token():
                return True

    def get_admin_token(self):
        return self.config["admin_token"]