import json, os

def writeJSON(filePath, data):
    with open(filePath, "w") as f:
        json.dump(data, f, indent=4)

def line2Calc(statsDict):
    #line2 calculation
    userList = statsDict["users"].keys()
    if not userList:
        print("Theres no data")
        return ("None", 0)
    userDict = {}
    for i in userList:
        y = statsDict["users"][i]["numbers"]
        userDict[i] = y
    foundUser = max(userDict, key=userDict.get)
    userCatches = userDict[foundUser]
    return (statsDict['users'][foundUser]['name'], userCatches)

def line3Calc(statsDict):
    #line3 calculation
    userList = statsDict["users"].keys()
    if not userList:
        print("Theres no data")
        return ("None", 0)
    userDict = {}
    for i in userList:
        y = statsDict["users"][i]["numbers"]
        userDict[i] = y
    foundUser = (min(userDict, key=userDict.get))
    userCatches = userDict[foundUser]
    return (statsDict['users'][foundUser]['name'], userCatches)

def shinyCalc(statsDict):
    userList = statsDict["users"].keys()
    if not userList:
        print("Theres no data")
        return ("None", 0)
    userDict = {}
    for i in userList:
        y = statsDict["users"][i]["shinys"]
        userDict[i] = y
    foundUser = (max(userDict, key=userDict.get))
    userCatches = userDict[foundUser]
    return (statsDict['users'][foundUser]['name'], userCatches)

def shinyTotal(statsDict):
    userList = statsDict["users"].keys()
    if not userList:
        print("Theres no data")
        return 0
    shinyNumber = 0
    for i in userList:
        shinyNumber += statsDict["users"][i]["shinys"]
    return shinyNumber

def line4Calc(statsDict):
    #line4 line5 line10 line11 calculations
    userList = statsDict["users"].keys()
    if not userList:
        print("Theres no data")
        return ("None", 0, 0, 0, 0)
    userDict = {}
    totalFails = 0
    for i in userList:
        y = statsDict["users"][i]["fails"]
        userDict[i] = y
        totalFails += y

    totalCatches = statsDict["total"]["number"]
    totalAttempts = totalCatches + totalFails
    percentFail = round(totalFails / totalAttempts * 100, 1)

    foundUser = (max(userDict, key=userDict.get))
    userCatches = userDict[foundUser]
    return (statsDict['users'][foundUser]['name'], userCatches, percentFail, totalCatches, totalFails)

def line6Calc(users_dict=None):
    #line6 calculation
    y = os.listdir("./data/bucket/")
    if not y:
        print("No buckets detected")
        return ("None", 0)
    typeDict = {}
    for i in y:
        filePath = "./data/bucket/" + i
        z = sum(1 for line in open(filePath)) -2
        typeDict[i] = z
    foundUser = (max(typeDict, key=typeDict.get))
    foundValue = typeDict[foundUser]
    print(f'foundUser = {foundUser}')
    return (users_dict[foundUser[:-5]], foundValue)

def combinedWeight(users_dict=None):
    weightDict = {}
    y = os.listdir("./data/bucket/")
    if not y:
        print("No buckets detected")
        return("None", 0)
    for i in y:
        shortName = i[:-5]
        totalWeight = 0
        filePath = "./data/bucket/" + i
        with open(filePath, "r") as f:
            data = json.load(f)
        for key in data.keys():
            totalWeight += data[key]
        weightDict[shortName] = round(totalWeight, 2)

    foundUser = (max(weightDict, key=weightDict.get))
    userCatches = weightDict[foundUser]
    return (users_dict[foundUser], userCatches)

def getWrStats(wrDict):
    #line7 line12?
    fishList = wrDict.keys()
    wrHolderList = []
    wrWeightsDict = {}
    for i in fishList:
        y = wrDict[i]["holder"]
        wrHolderList.append(y)

        w = wrDict[i]["weight"]
        f = i
        wrWeightsDict[f] = w

    biggestFishN = (max(wrWeightsDict, key=wrWeightsDict.get))
    biggestFishW = wrWeightsDict[biggestFishN]
    mostRecords = max(set(wrHolderList), key = wrHolderList.count)
    return (mostRecords, biggestFishN, biggestFishW)

def fishCaughtMost(statsDict):
    fishList = statsDict["fishes"].keys()
    fishListDict = {}
    for i in fishList:
        y = statsDict["fishes"][i]["number"]
        fishListDict[i] = y
    mostCaught = (max(fishListDict, key=fishListDict.get))
    mostCaughtNum = fishListDict[mostCaught]
    return (mostCaught, mostCaughtNum)

def fishCaughtLeast(statsDict):
    fishList = statsDict["fishes"].keys()
    fishListDict = {}
    for i in fishList:
        y = statsDict["fishes"][i]["number"]
        fishListDict[i] = y
    leastCaught = (min(fishListDict, key=fishListDict.get))
    leastCaughtNum = fishListDict[leastCaught]
    return (leastCaught,leastCaughtNum)

def classPercentages(statsDict):
    class1 = statsDict["total"]["1"]
    class2 = statsDict["total"]["2"]
    class3 = statsDict["total"]["3"]
    class4 = statsDict["total"]["4"]
    class5 = statsDict["total"]["5"]
    class6 = statsDict["total"]["6"]
    class7 = statsDict["total"]["7"]
    total = class1+class2+class3+class4+class5+class6+class7
    class1P = round(class1 / total * 100, 1)
    class2P = round(class2 / total * 100, 1)
    class3P = round(class3 / total * 100, 1)
    class4P = round(class4 / total * 100, 1)
    class5P = round(class5 / total * 100, 1)
    class6P = round(class6 / total * 100, 1)
    class7P = round(class7 / total * 100, 1)
    classT = (class1P, class2P, class3P, class4P, class5P, class6P, class7P)
    return classT

def fishStats(uid, fish, weight, fishClass, shiny, username):
    with open("./data/fishstats.json", "r") as f:
        data = json.load(f)
    fishClassStr = str(fishClass)
    #add to the fish specific total
    data["fishes"][fish]["number"] += 1
    #add to the game total
    data["total"]["number"] += 1
    data["total"][fishClassStr] += 1
    #add user specific data
    if uid not in data["users"]:
        data["users"][uid] = {
            "name": username,
            "numbers": 0,
            "fails": 0,
            "shinys": 0
        }
    elif "name" not in data["users"][uid]:
        data["users"][uid]["name"] = username
    data["users"][uid]["numbers"] += 1
    #after statprofile creation add shinys mess...
    if shiny:
        data["users"][uid]["shinys"] += 1
        print(f'{username} got a SHINY {fish} at {weight}')
    writeJSON("./data/fishstats.json", data)

def listFishStats(users_dict):
    with open("./data/fishstats.json", "r") as f1:
        statsDict = json.load(f1)
    with open("./data/fishwr.json", "r") as f2:
        wrDict = json.load(f2)

    #line2
    activeUser, activeCatches = line2Calc(statsDict)
    #line3
    LactiveUser, LactiveCatches = line3Calc(statsDict)
    #line4 line5 line10 line11
    unluckyUser, mostFails, percentFail, totalCatchesX, totalFailsX = line4Calc(statsDict)
    #line6
    longestBucket, longestNumb = line6Calc(users_dict)
    #line7 line12?
    mostWRs, biggestFishNa, biggestFishWe  = getWrStats(wrDict)
    #line8 line9
    mostFish, mostFishN = fishCaughtMost(statsDict)
    leastFish, leastFishN = fishCaughtLeast(statsDict)
    #line13-14
    classT = classPercentages(statsDict)
    #shinys
    shinyUser, shinyCatches = shinyCalc(statsDict)
    shinyTotalCatch = shinyTotal(statsDict)
    #combined total weight leader
    totalWeightUser, totalWeightUserWeight = combinedWeight(users_dict)


    msg = f'''---- Fishing Simulator Statistics ----
Most active fisher : {activeUser} {activeCatches} catch(es)
Least active fisher : {LactiveUser} {LactiveCatches} catch(es)
Unluckiest fisher : {unluckyUser} {mostFails} fails
Percent of failed casts : {percentFail}% (total)
Most diverse fisher : {longestBucket} {longestNumb} types in bucket
Most caught shinies : {shinyUser} ({shinyCatches})
Most world records : {mostWRs}
Most caught fish : {mostFish} ({mostFishN})
Least caught fish : {leastFish} ({leastFishN})
Total caught fish : {totalCatchesX}
Total caught shinies : {shinyTotalCatch}
Top total weight in bucket : {totalWeightUser} {totalWeightUserWeight} lbs
Total failed casts : {totalFailsX}')
Biggest fish ever caught : {biggestFishNa} at {biggestFishWe} lbs
Class percentages class1: {classT[0]}% class2: {classT[1]}% class3: {classT[2]}% class4: {classT[3]}%
class5: {classT[4]}% class6: {classT[5]}% class7: {classT[6]}%'''

    return msg
