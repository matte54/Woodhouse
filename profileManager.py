import json

def writeJSON(filePath, data):
    with open(filePath, "w") as f:
        json.dump(data, f, indent=4)
        f.close()

def getFishValues(fishName, className):
    filePath = (f"./data/fishdata/class{className}.json")
    with open(filePath, "r") as f:
        data = json.load(f)
    return(data[fishName]['value'], data[fishName]['xp'])


def handleMoney(userId, money=0, fishName="", classInt=0):
    if classInt != 0:
        value, xp = getFishValues(fishName, classInt)
    filePath = f"./data/fishprofiles/{userId}.json"
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    if classInt != 0:
        data["money"] += value
    else:
        data["money"] += money
    writeJSON(filePath, data)

def profileHandler(userId, fishName, className):
    filePath = f"./data/fishprofiles/{userId}.json"
    value, xp = getFishValues(fishName, className)
    #check if profile excist then load if not create.
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f'{userId}.json Not found...creating')
        data = {"money": 0, "currentXp": 0, "xpCap": 25, "level": 1, "gear": []}
        writeJSON(filePath, data)
    #add xpvalue
    userXp = data["currentXp"]
    currentXpCap = data["xpCap"]
    if userXp + xp >= currentXpCap:
        xpDiff = (userXp + xp) - currentXpCap
        data["level"] += 1
        data["currentXp"] = xpDiff
        data["xpCap"] += (10 + data["level"])
        print(f'DING! {userId} is now level {data["level"]}')
    else:
        data["currentXp"] += xp
        print(f'{xp} XP gained {data["currentXp"]}/{data["xpCap"]}')
    writeJSON(filePath, data)
