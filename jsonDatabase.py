# storage.py
from filelock import FileLock
import json, os

# DB_FILE = os.path.join(pathlib.Path(__file__).parent,"link_token_to_userId.json")

def read(DB_FILE):
    if not os.path.exists(DB_FILE):
        return {}
    # with FileLock(DB_FILE):
    with open(DB_FILE, "r") as f:
        return json.load(f)

def write(DB_FILE, data):
    with open(DB_FILE, "w") as f: 
        print("WRITING", data, DB_FILE)
        json.dump(data, f)

def pop(DB_FILE, key):
    onAuthEvent = read(DB_FILE)
    onAuthEvent.pop(key, None)
    write(DB_FILE, onAuthEvent)
    # print("Stored new on_auth_event", onAuthEvent)

def set(DB_FILE, key, value):
    onAuthEvent = read(DB_FILE)
    onAuthEvent[key] = value
    write(DB_FILE, onAuthEvent)
    # print("Stored new on_auth_event", onAuthEvent)

def createDatabase(DBFILE):
    def actioner(actionFunction, *args):
        return actionFunction(DBFILE, *args)
    return actioner