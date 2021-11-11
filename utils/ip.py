import hashlib

def encode(ip: str):
    return hashlib.sha256(ip.encode()).hexdigest()