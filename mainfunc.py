import random, datetime
import io
import markovify
import requests
import json, os
from lxml import etree as ET
from discord import Embed

#Fishing Lists
fishClass1 = ["Tin can", "Old shoe", "Rusty dagger", "Seaweed", "Magikarp"]
jokeClass1 = ["This can can!", "Where is the other one?", "Old murder weapon?", "Those fish must be pretty high", "He casts splash...its super effective!"]
fishClass2 = ["Bitterling", "Pale chub", "Goldfish", "Pop-eyed goldfish", "Killifish", "Tadpole", "Guppy", "Nibble fish", "Neon tetra", "Rainbowfish", "Sea butterfly", "Sea horse", "Clown fish"]
jokeClass2 = ["It's mad at me, but only a little", "That name seems a bit judgy...", "It's worth its weight in fish!", "It looks so...surprised!", "The streams are safe again.", "I'm sure it will grow on me.", "Welcome to the team, newbie!", "Come to think of it, I could use a bite!", "Wasn't hard to track.", "Where's my pot of goldfish?", "Try not to confuse it for a sea moth!", "But...where's its sea jockey?", "How many can fit in a carfish?"]
fishClass3 = ["Crucian carp", "Ranchu goldfish", "Crawfish", "Frog", "Freshwater goby", "Loach", "Bluegill", "Pond smelt", "Mitten crab", "Angelfish", "Betta", "Piranha", "Surgeonfish", "Butterfly fish", "Anchovy", "Horse mackerel", "Barreleye"]
jokeClass3 = ["My skills are sharp!", "But I prefer balsamicu goldfish!", "Or else it's a lobster, and I'm a giant!", "Or it's a new neighbor...and I have some apologizing to do.", "Time to go bye-bye!", "It's ... looking at me with reproach.", "Do you think it calls me 'pinklung'?", "Whoever smelt it, dealt it!", "One more and I'm ready for winter!", "That other fish told me to do it!", "I betta not drop it!", "Sure hope it was the only one!", "Scalpel! Forceps! Fish hook!", "Did it change from a caterpillar fish?", "Stay away from my pizza!", "Of course, Mack...er..el.", "Like eyeing fish in a barrel!"]
fishClass4 = ["Dace", "Yellow perch", "Tilapia", "Sweetfish", "Cherry salmon", "Char", "Golden trout", "Zebra turkeyfish", "Blowfish", "Puffer fish", "Barred knifejaw", "Dab", "Squid"]
jokeClass4 = ["Hope I have some space!", "Those yellow birds have to sit somewhere!", "It makes me happy-a!", "Hope it's not artificially sweet!", "It's the perfect topper for a marlin sundae!", "Now I'm gonna sit on it!", "But the real treasure? Friendship.", "Land, air, water-make up your mind!", "I'm blown away!", "I thought you would be tougher, fish!", "They must have a hard time eating!", "Not bad!", "Do they... not actually 'bloop'?"]
fishClass5 = ["Carp", "Koi", "Soft-shelled turtle", "Snapping Turtle", "Catfish", "Giant snakehead", "Black bass", "Salmon", "Arowana", "Saddled bichir", "Red snapper", "Football fish"]
jokeClass5 = ["If I catch another they can carpool", "I don't know why it's so shy... or such a bad speller...", "I should take a shellfie!", "How can it snap without fingers?", "I'm more of a dogfish person...", "Um...but I asked for a medium?", "The most metal of all fish!", "It's all upstream from here!", "I'd make a joke, but I don't 'wana.", "And me without my tiny riding crop...", "It looks pretty dapper!", "Some countries call it a soccer fish!"]
fishClass6 = ["Pike", "Stringfish", "King salmon", "Dorado", "Gar", "Sea bass", "Olive flounder", "Giant trevally", "Mahi-mahi", "Ray"]
jokeClass6 = ["Think a swordfish would be up for a duel?", "Five more and I'll have a guitarfish!", "I caught a king salmon! Checkmate!", "I say 'dorado', you say 'doraydo'.", "Yar! It's a gar! Har har!", "No, wait- it's at least a C+!", "That's not the pits!", "Yeah, I'm pretty well-traveled.", "It's all mahine-mahine.", "A few more and I'll have a tan!"]
fishClass7 = ["Arapaima", "Sturgeon", "Napoleonfish", "Tuna", "Blue marlin", "Ocean sunfish", "Saw shark", "Hammerhead shark", "Great white shark", "Whale shark", "Suckerfish", "Oarfish", "Coelacanth"]
jokeClass7 = ["How did it get here? Arapaiknow!", "Wonder if it can perform sturgery...", "It’s not as big as it thinks!", "It's a little off-key!", "Listen to this fish. it's got a point.", "Good thing I'm wearing ocean sunscreen!", "You could call it a sea saw!", "I hit the nail on the head!", "Watch out for its jaws!", "I'm tellin' ya, it was thiiiiiiiiiiiiiiiiiiiis big!", "I thought it was a shark! Oh, wait - now I get it. 'Sucker'...", "I hope I catch morefish!", "Think positive! Be a coela-CAN!"]

#compile text model for random generation
with open("generalchat.txt", encoding='utf-8') as f:
    text = f.read()
text_model = markovify.NewlineText(text)
text_model.compile()

# Old randomline system
#def random_line(fname):
#    lines = open(fname, encoding='utf8').read().splitlines()
#    x = random.choices(lines, k=10)
#    return(x)

def get_speech(client):
    #Markovify instead of random line.
    r = []
    for l in range(5):
        r.append(text_model.make_sentence())
    for k in range(5):
        r.append(text_model.make_short_sentence(15, tries=100))
    #Short sentences leaves None entries ghetto remove those...
    cla_list = []
    for val in r:
        if val != None:
            cla_list.append(val)
    r = cla_list
    washing = []
    washing.extend(r)
    emojis = client.emojis
    emoji_names = [emoji.name for emoji in client.emojis]
    #add 10 emoji choices
    sEmo = random.choices(emoji_names, k=10)
    sEmo = [':%s:' % emoji_name for emoji_name in sEmo]
    washing.extend(sEmo)

    for i, emoji in enumerate(emojis):
        for j, reply in enumerate(washing):
            if f':{emoji.name}:' in reply:
                old_text = f':{emoji.name}:'
                new_text = f'<:{emoji.name}:{emoji.id}>'
                washing[j] = reply.replace(old_text, new_text)
    x = random.choice(washing)
    return (x)

# Test for markovify, left in for the $speech command just because
def ranswer():
    return (text_model.make_sentence())

def get_holiday():
    req = requests.get('https://www.checkiday.com/rss.php?tz=Europe/Stockholm')
    result = ET.fromstring(req.content)
    things = [thing[1].text for thing in result.iter('item')]
    return random.choice(things)

def cast_line(discordId):
    #define variables n stuff
    uid = str(discordId)
    fileDir = "./data/fishdata/"
    fishFiles = ["class1.json", "class2.json", "class3.json", "class4.json", "class5.json", "class6.json", "class7.json"]

    #pick random fish with weighted chances
    chosenClass = random.choices(fishFiles, weights=(38, 19, 15, 12, 7, 6, 3))
    filePath = fileDir + chosenClass[0]
    #access json should never error but anyways?
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
            #print(f'LOADED {filePath}!')
    except FileNotFoundError:
        return(f'ERROR {filePath} NOT FOUND SOMETHING IS WRONG HERE...')

    #Ugly data converting back and forth cause i dont know syntax
    z = random.choice(list(data))
    j = data[z]['joke']
    wL = data[z]['weightLow']
    wH = data[z]['weightHigh']
    #Triangular weighted random weight test.
    mid = wL+wH / 2
    w = round(random.triangular(wL, wH, mid),2)
    c = chosenClass[0][:-5]


    #Make the only fish once and hour mark.
    now = datetime.datetime.now()
    f = open('./data/fishTime/'+uid, "w")
    f.write(str(now.hour))
    f.close()

    #new rogue embedd System
    wr, holder = get_wr(z)  # get the current wr if any
    #changed check_wr to this if statement
    if holder == "None":    # assuming if no wr we get back weight is 0.0 and holder is "None"
        wr, holder = 0.0, ""
    elif w > wr:              # if new fish is wr, write it to file
        write_wr(uid, z, w)
    q = addFish(discordId, z, w)
    cI = int(c[5:])
    x = fishing_embed(uid, z, j, cI, w, old_pb=q, old_wr=wr, dethroned=holder)
    return(x)

    #Old System
    #check WR
    #wr = check_wr(uid, z, w)
    #u = "CASTS THEIR LINE AND CATCHES A " + z + " " + c + "\n" + j + "\n" + "WEIGHT (" + str(w) + ") LBS \n" + wr
    #return(u.upper(), z, w)

def fishOff():
    path = "./data/bucket/"
    highscoreDict = {}
    x = os.listdir(path)
    if len(x) != 0:
        for i in x:
            filePath = path + i
            with open(filePath, "r") as f:
                data = json.load(f)
                sort_bucket = sorted(data.items(), key=lambda x: x[1], reverse=True)
                sortdict = dict(sort_bucket)
                topFish = next(iter(sortdict))
                topFishWeight = sortdict[topFish]
                nameFix = i[:-5]
                highscoreDict[nameFix + ' - ' + topFish] = topFishWeight

        sort_score = sorted(highscoreDict.items(), key=lambda x: x[1], reverse=True)
        sort_score_dict = dict(sort_score)
        #Code to return the winner for future winnerlist.
        y = next(iter(sort_score_dict))
        z = str(sort_score_dict[y])
        winner = y.upper() + ' - '+ z + ' LBS'

        x = ""
        for i in sort_score_dict:
            x += i.upper() + ' - ' + str(sort_score_dict[i]) + ' LBS\n'
        return(x, winner)
    else:
        return("There is no buckets!")

def bucket(discordId):
    discordIdStr = str(discordId)
    jsonFile = discordIdStr + '.json'
    filePath = "./data/bucket/"+jsonFile
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
            sort_bucket = sorted(data.items(), key=lambda x: x[1], reverse=True)
            sortdict = dict(sort_bucket)
            x = discordIdStr.upper() + "s BUCKET(TOP 10)\n"
            limit = 0
            for i in sortdict:
                x += i.upper() + ' - ' + str(sortdict[i]) + ' LBS\n'
                limit += 1
                if limit == 10:
                    break
    except FileNotFoundError:
        return("No fish in the bucket yet , go catch some!")
    return(x)

def addFish(discordId, fish, weight):
    discordIdStr = str(discordId)
    jsonFile = discordIdStr + '.json'
    filePath = "./data/bucket/"+jsonFile
    #print(f'Loading file...{filePath}')
    if os.path.isfile(filePath) == True:
        #print(f'File found!')
        with open(filePath, "r") as f:
            data = json.load(f)
            if fish in data:
                #print(f"That fish type is in the bucket already.")
                if data[fish] < weight:
                    x = (f'NEW RECORD {fish}! This new one was {weight} the one in your bucket was only {data[fish]}')
                    oldPb = data[fish]
                    data[fish] = weight
                    writeJSON(filePath, data)
                    #new rogue
                    return(oldPb)
                else:
                    x = (f'This {fish} was only {weight}, you already have one at {data[fish]}')
                    currentPb = data[fish]
                    return(currentPb)
            else:
                x = (f"New fish type! great addition to your bucket!")
                data[fish] = weight
                writeJSON(filePath, data)
                return(0.0)
    else:
        x = ""
        #print(f"JSON not found! Creating...")
        data = {fish: weight}
        writeJSON(filePath, data)
    #old system
    #return(x)
    return(0.0)


def fishscore():
    filePath = "./data/fishoffwinners.json"
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
            x = " ***** - FISHOFF WINNERS - *****\n"
            limit = 0
            for i in data:
                x += str(data[i]) + ' POUNDS\n'
                limit += 1
                if limit == 10:
                    break
    except FileNotFoundError:
        return("No previous winners yet!")
    return(x)

def fishOffHandler():
    dir = './data/bucket'
    now = datetime.datetime.now()
    lastMonth = now - datetime.timedelta(days=now.day)
    monthStr = lastMonth.strftime("%b")
    yearStr = lastMonth.strftime("%Y")
    #nowdebug = 1
    #if nowdebug == 1:
    if now.day == 1:
        print(f'Today is the first of the month!')

        path = "./data/bucket/"
        highscoreDict = {}
        x = os.listdir(path)
        for i in x:
            filePath = path + i
            with open(filePath, "r") as f:
                data = json.load(f)
                sort_bucket = sorted(data.items(), key=lambda x: x[1], reverse=True)
                sortdict = dict(sort_bucket)
                topFish = next(iter(sortdict))
                topFishWeight = sortdict[topFish]
                nameFix = i[:-5]
                highscoreDict[nameFix + ' - ' + topFish] = topFishWeight
                sort_score = sorted(highscoreDict.items(), key=lambda x: x[1], reverse=True)
                sort_score_dict = dict(sort_score)
                #Code to return the winner for future winnerlist.
                y = next(iter(sort_score_dict))
                z = str(sort_score_dict[y])

        winnertext = monthStr + " " + yearStr + " " + y + " " + z

        Key = monthStr+yearStr
        filePath2 = "./data/fishoffwinners.json"
        with open(filePath2, "r") as f2:
            data2 = json.load(f2)
            if Key in data2:
                print(f'{Key} entry already exists...ignoring')
            else:
                print(f'A fishoff winner been crowned {winnertext}')
                data2[Key] = winnertext
                writeJSON(filePath2, data2)
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))
                    print(f'Deleting {f}')
                return(winnertext)
    else:
        print(f'Today is NOT the first of the month, its {now.day}...keep fishing')


def get_wr(fish):
    filePath = "./data/fishwr.json"
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return (f'ERROR {filePath} NOT FOUND SOMETHING IS WRONG HERE...')
    return data[fish]['weight'], data[fish]['holder']


def write_wr(uid, fish, weight):
    filePath = "./data/fishwr.json"
    try:
        with open(filePath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return (f'ERROR {filePath} NOT FOUND SOMETHING IS WRONG HERE...')
    data[fish]['weight'] = weight
    data[fish]['holder'] = uid
    writeJSON(filePath, data)
    print(f'Wrote to file {filePath}')

def writeJSON(filePath, data):
    with open(filePath, "w") as f:
        json.dump(data, f, indent=4)
        f.close()
    #print(f'Finished writing {filePath}')

def fishing_embed(username, fish, joke, fish_class, weight, old_pb=0.0, old_wr=0.0, dethroned=""):
    """Create a discord embed of the caught fish.

    Note if old_wr is provided remember to also provide the dethroned parameter.

    :param username: The user that caught the fish
    :type username: str
    :param fish: The name of the fish
    :type fish: str
    :param joke: It's a joke
    :type joke: str
    :param fish_class: The class of fish
    :type fish_class: int
    :param weight: The weight of the fish
    :type weight: float
    :param old_pb: The weight of the user's previous record if applicable, defaults to 0.0
    :type old_pb: float
    :param old_wr: The wright of the previous world record if applicable, defaults to 0.0
    :type old_wr: float
    :param dethroned: The name of the previous record holder if applicable, defaults to ""
    :type dethroned: str

    :return: The created embed
    :rtype: discord.Embed
    """

    embed = Embed()
    n = 'n' if fish.lower()[0] in 'aeiou' else ''
    embed.title = f"{username} caught a{n} {fish}!"
    embed.description = f"*{joke}*"
    embed.colour = 0x99ff
    embed.add_field(name="Class", value=f"**{fish_class}**", inline=True)
    embed.add_field(name="Weight", value=f"**{weight}**", inline=True)
    if old_pb == 0.0:
        embed.add_field(name="New fish type!", value="Great addition to your bucket!")
    elif weight > old_pb:
        embed.add_field(name="NEW RECORD!", value=f"*Your previous one was only {old_pb} lbs*")
    else:
        embed.add_field(name=f"Releasing {fish}...", value=f"You already have one at {old_pb} lbs!")
    if old_wr == 0.0 and dethroned == "":
        embed.add_field(name="NEW WORLD RECORD!", value=f"*You caught the first {fish}!*")
    elif old_wr > 0.0 and dethroned != "":
        embed.add_field(name="NEW WORLD RECORD!", value=f"*Previous record was {old_wr} lbs by {dethroned}*")
    else:
        print(f"Something weird happened old_wr: {old_wr} dethroned: {dethroned}")
    fishWithoutSpaces = fish.replace(" ", "")
    icon_url = f"http://thedarkzone.se/fishicons/{fishWithoutSpaces}.png"
    embed.set_thumbnail(url=icon_url)
    return embed
