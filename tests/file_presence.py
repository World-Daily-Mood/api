from os.path import exists
import sys

sys.path.insert(1, "./")
from utils import config
cnf = config.Config()

def _check_file(filepath):
    return exists(filepath)

def main():
    configfiles = cnf.get_configfiles()

    for file in configfiles:
        if _check_file(file) != True:
            return [2, f"File missing - {file}"]
    
    return ["0", None]

if __name__ == "__main__":
    main()