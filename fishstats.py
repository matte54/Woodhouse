import json, os

def writeJSON(filePath, data):
    with open(filePath, "w") as f:
        json.dump(data, f, indent=4)
        f.close()


def fishStats(uid, fish, weight, fishClass):
    with open("./data/fishstats.json", "r") as f:
        data = json.load(f)

    #add to the fish specific total
    data["fishes"][fish]["number"] += 1
    #add to the game total
    data["total"]["number"] += 1
    #add user specific data
    if uid not in data["users"]:
        data["users"][uid] = {}
        data["users"][uid]["numbers"] = 0
        data["users"][uid]["fails"] = 0
    data["users"][uid]["numbers"] += 1
    writeJSON("./data/fishstats.json", data)
