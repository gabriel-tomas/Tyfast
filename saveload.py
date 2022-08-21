import json

def save(object, file=None):
    with open(file, "w") as write:
        json.dump(object, write, indent=4)

def load():
    with open("config.json", "r") as read:
        data = json.load(read)
    return data