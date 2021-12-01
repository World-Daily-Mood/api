import random
import string

def generate():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))