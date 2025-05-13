import os
import time
import json

CACHE_FILE = "token_cache.json"

def save_token(token, expiry):
    with open(CACHE_FILE, "w") as f:
        json.dump({"token": token, "expiry": expiry}, f)

def load_token():
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r") as f:
        data = json.load(f)

    if data["expiry"] > time.time():
        return data["token"]
    return None
