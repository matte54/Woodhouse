import json, random

def writeJSON(filePath, data):
    with open(filePath, "w") as f:
        json.dump(data, f, indent=4)
        f.close()

def getUserInfo(userId):
    filePath = f"./data/fishprofiles/{userId}.json"
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
        money = data["money"]
        lvl = data["level"]
        exp = data["currentXp"]
        xpCap = data["xpCap"]
        txt = f'-- Lvl: {lvl} - Exp: {exp}/{xpCap} - Bells: {money} --'
    except FileNotFoundError:
        txt = f'-- Lvl: 1 - Exp: 0/25 - Bells: 0 --'
        return(txt)
    return(txt)

def getFishValues(fishName, className, fishWeight):
    filePath = (f"./data/fishdata/class{className}.json")
    with open(filePath, "r") as f:
        data = json.load(f)
    money = data[fishName]['value']
    xp = data[fishName]['xp']
    if fishWeight != 0:
        wL = data[fishName]["weightLow"]
        wH = data[fishName]["weightHigh"]
        mid = (wL + wH) / 2
        if fishWeight < mid:
            xp -= 1
            xp -= random.randint(0,2)
            if xp < 0:
                xp = 0

            money -= 1
            money -= random.randint(0,2)
            if money < 0:
                money = 0
        if fishWeight > mid:
            xp += 1
            xp += random.randint(0,2)

            money += 1
            money += random.randint(0,2)

    return(money, xp)

def getLevel(userId):
    filePath = f"./data/fishprofiles/{userId}.json"
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
        x = data["level"]
    except FileNotFoundError:
        return(1)
    return(x)

def handleMoney(userId, money=0, fishName="", classInt=0, fishWeight=0):
    if classInt != 0:
        value, xp = getFishValues(fishName, classInt, fishWeight)
    filePath = f"./data/fishprofiles/{userId}.json"
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return
    if classInt != 0:
        data["money"] += value
        print(f'{value} money')
    else:
        data["money"] += money
        print(f'{money} money')
        value = 0
    writeJSON(filePath, data)
    return(value)

def profileHandler(userId, fishName, className, fishWeight):
    filePath = f"./data/fishprofiles/{userId}.json"
    value, xp = getFishValues(fishName, className, fishWeight)
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
    return(value, xp)
