import json


def save(object=None, file="config.json"):
    try:
        content = load()
        total = {}
        for key, value in content.items():
            print(key in object and value not in object)
            if key in object and value not in object:
                total = object
            else:
                total[key] = value
        with open(file, "w") as write:
            json.dump(total, write, indent=4)
    except Exception:
        with open(file, "w") as write:
            json.dump(object, write, indent=4)

def load(file="config.json"):
    try:
        with open(file, "r") as read:
            data = json.load(read)
    except Exception as error:
        data = ""
    return data

def save_score(object=None, difficulty=None, file="score.json"):
    try:
        last_point = load("score.json")
    except:
        last_point = None
    if last_point:
        items_total = {}
        for key, point in last_point.items():
            if key == difficulty:
                if object[difficulty] > point:
                    items_total[difficulty] = object[difficulty]
                else:
                    items_total[key] = point
            else:
                items_total[key] = point
        with open(file, "w") as write:
            json.dump(items_total, write, indent=4) 
        return items_total           
    else:
        with open(file, "w") as write:
            json.dump(object, write, indent=4)
        return object
        

if __name__ == "__main__":
    save_score({"easy":4, "medium":7, "hard":0}, difficulty="medium")