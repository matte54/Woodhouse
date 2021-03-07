import json, os

def writeJSON(filePath, data):
    with open(filePath, "w") as f:
        json.dump(data, f, indent=4)
        f.close()

def line2Calc(statsDict):
    #line2 calculation
    userList = statsDict["users"].keys()
    if not userList:
        print("Theres no data")
        return("None", 0)
    userDict = {}
    for i in userList:
        y = statsDict["users"][i]["numbers"]
        userDict[i] = y
    foundUser = (max(userDict, key=userDict.get))
    userCatches = userDict[foundUser]
    return(foundUser, userCatches)

def line3Calc(statsDict):
    #line3 calculation
    userList = statsDict["users"].keys()
    if not userList:
        print("Theres no data")
        return("None", 0)
    userDict = {}
    for i in userList:
        y = statsDict["users"][i]["numbers"]
        userDict[i] = y
    foundUser = (min(userDict, key=userDict.get))
    userCatches = userDict[foundUser]
    return(foundUser, userCatches)

def line4Calc(statsDict):
    #line4 line5 line10 line11 calculations
    userList = statsDict["users"].keys()
    if not userList:
        print("Theres no data")
        return("None", 0, 0, 0, 0)
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
    return(foundUser, userCatches, percentFail, totalCatches, totalFails)

def line6Calc():
    #line6 calculation
    y = os.listdir("./data/bucket/")
    if not y:
        print("No buckets detected")
        return("None", 0)
    typeDict = {}
    for i in y:
        filePath = "./data/bucket/" + i
        z = sum(1 for line in open(filePath)) -2
        typeDict[i] = z
    foundUser = (max(typeDict, key=typeDict.get))
    foundValue = typeDict[foundUser]
    return(foundUser[:-5], foundValue)


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
    return(mostRecords, biggestFishN, biggestFishW)

def fishCaughtMost(statsDict):
    fishList = statsDict["fishes"].keys()
    fishListDict = {}
    for i in fishList:
        y = statsDict["fishes"][i]["number"]
        fishListDict[i] = y
    mostCaught = (max(fishListDict, key=fishListDict.get))
    mostCaughtN = fishListDict[mostCaught]
    return(mostCaught, mostCaughtN)

def fishCaughtLeast(statsDict):
    fishList = statsDict["fishes"].keys()
    fishListDict = {}
    for i in fishList:
        y = statsDict["fishes"][i]["number"]
        fishListDict[i] = y
    leastCaught = (min(fishListDict, key=fishListDict.get))
    leastCaughtN = fishListDict[leastCaught]
    return(leastCaught, leastCaughtN)

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
    print(class2P)
    classT = (class1P, class2P, class3P, class4P, class5P, class6P, class7P)
    return(classT)

def fishStats(uid, fish, weight, fishClass):
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
        data["users"][uid] = {}
        data["users"][uid]["numbers"] = 0
        data["users"][uid]["fails"] = 0
    data["users"][uid]["numbers"] += 1
    writeJSON("./data/fishstats.json", data)

def listFishStats():
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
    longestBucket, longestNumb = line6Calc()
    #line7 line12?
    mostWRs, biggestFishNa, biggestFishWe  = getWrStats(wrDict)
    #line8 line9
    mostFish, mostFishN = fishCaughtMost(statsDict)
    leastFish, leastFishN = fishCaughtLeast(statsDict)
    #line13-14
    classT = classPercentages(statsDict)


    line1 = (f'---- Fishing Simulator Statistics ----')
    line2 = (f'\nMost active fisher : {activeUser} {activeCatches} catch(es)')
    line3 = (f'\nLeast active fisher : {LactiveUser} {LactiveCatches} catch(es)')
    line4 = (f'\nUnluckiest fisher : {unluckyUser} {mostFails} fails')
    line5 = (f'\nPercent of failed casts : {percentFail}% (total)')
    line6 = (f'\nMost diverse fisher : {longestBucket} {longestNumb} types in bucket')
    line7 = (f'\nMost world records : {mostWRs}')
    line8 = (f'\nMost caught fish : {mostFish} ({mostFishN})')
    line9 = (f'\nLeast caught fish : {leastFish} ({leastFishN})')
    line10 = (f'\nTotal caught fish : {totalCatchesX}')
    line11 = (f'\nTotal failed casts : {totalFailsX}')
    line12 = (f'\nBiggest fish ever caught : {biggestFishNa} at {biggestFishWe} lbs')
    line13 = (f'\nClass percentages class1: {classT[0]}% class2: {classT[1]}% class3: {classT[2]}% class4: {classT[3]}%')
    line14 = (f'\nclass5: {classT[4]}% class6: {classT[5]}% class7: {classT[6]}%')

    x = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9 + line10 + line11 + line12 + line13 + line14
    return(x)
