from utils import config

cnf = config.Config()

def is_valid(mood):
    if mood in cnf.get_valid_moods():
        return True