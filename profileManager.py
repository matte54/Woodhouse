
import json, random, os

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
        return txt
    return txt

def getFishValues(fishName, className, fishWeight):
    filePath = f"./data/fishdata/class{className}.json"
    with open(filePath, "r") as f:
        data = json.load(f)
    money = data[fishName]['value']
    xp = data[fishName]['xp']
    if fishWeight != 0:
        wL = data[fishName]["weightLow"]
        wH = data[fishName]["weightHigh"]
        mid = (wL + wH) / 2
        if fishWeight < mid:
            xp -= random.randint(0,1)
            xp -= random.randint(0,2)
            if xp < 0:
                xp = 0

            money -= random.randint(0,1)
            money -= random.randint(0,2)
            if money < 0:
                money = 0
        if fishWeight > mid:
            xp += random.randint(0,1)
            xp += random.randint(0,2)

            money += random.randint(0,1)
            money += random.randint(0,2)

    return (money, xp)

def getLevel(user_obj):
    filePath = f"./data/fishprofiles/{user_obj.id}.json"
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
        x = data["level"]
    except FileNotFoundError:
        return 1
    return x

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
        #print(f'adding {value} of {fishName} money to {userId}')
    else:
        data["money"] += money
        #print(f'adding {money} money to {userId}')
        value = 0
    writeJSON(filePath, data)
    return value

def profileHandler(userId, fishName, className, fishWeight):
    filePath = f"./data/fishprofiles/{userId}.json"
    value, xp = getFishValues(fishName, className, fishWeight)
    #check if profile exists then load, if not create.
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
    dinged = 0
    if userXp + xp >= currentXpCap:
        xpDiff = (userXp + xp) - currentXpCap
        data["level"] += 1
        data["currentXp"] = xpDiff
        data["xpCap"] += (10 + data["level"])
        dinged = data["level"]
        #print(f'DING! {userId} is now level {data["level"]}')
    else:
        data["currentXp"] += xp
        #print(f'{xp} XP gained {data["currentXp"]}/{data["xpCap"]}')
    writeJSON(filePath, data)
    return (value, xp, dinged)

def buyCast(user_obj):
    userId = str(user_obj.id)
    if not os.path.isfile(f"./data/fishTime/{userId}"):
        return False
    filePath = f"./data/fishprofiles/{userId}.json"
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return False
    userMoney = data["money"]
    if userMoney < 50:
        return False
    data["money"] -= 50
    if os.path.isfile(f"./data/fishTime/{userId}"):
        os.remove(f"./data/fishTime/{userId}")
    writeJSON(filePath, data)
    return True
