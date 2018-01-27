import json

def load_json(file):
    try:
        with open(file, "r") as f:
            jsonObject = json.load(f)
        return(jsonObject)
    except FileNotFoundError:
        return None

def save_json(file, jsonObject):
    with open(file, "w") as f:
        json.dump(jsonObject, f, indent=2, sort_keys=True)
