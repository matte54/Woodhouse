from difflib import SequenceMatcher
import time
import os
import random

#### sentence filtering stuff
nopeChars = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
avoidwordlist = []
avoidpath = "./avoidwords.txt"
with open(avoidpath, 'r' , encoding='UTF-8') as avoidfile:
    avoidtext = avoidfile.read().splitlines()
for w in avoidtext:
    avoidwordlist.append(w.lower())

###load data from reddit
texte = ""
logfolderpath = "./rdata/"
for path, dirs, files in os.walk(logfolderpath):
    pass
for e in files:
    with open(f'./rdata/{e}', 'r' , encoding='UTF-8') as f:
        texte += f.read()

text = texte.splitlines()

data = []
for i in text:
    data.append((i.split(" / ")))
#print(f'main database has {len(data)} entries.')


def rspeak(question):
    data2 = []
    i = question.lower()
    #check for illeagal chars
    for ele in i:
        if ele in nopeChars:
            i = i.replace(ele, '')

    longestword = i.split()
    #word filtering
    removedList = []
    for wordsx in longestword:
        if wordsx in avoidwordlist:
            removedList.append(wordsx)
    # remove words in separate loop
    for w2 in removedList:
        longestword.remove(w2)
    if removedList:
        print(f'Removed words: {removedList}')
    #Get the longest word
    xa = sorted(longestword, key=len)
    if not xa:
        return f'All those words are ill-eagle...', f'```yaml\nERROR: All words in input where filtered out!```'
    print(xa)
    longestword1 = xa[-1]
    if len(xa) >= 2:
        leastlongestword = xa[-2]

    for l in data:
        a = l[0].split()
        if longestword1 in a:
            data2.append(l)

    #check the next least longestword?
    if not data2:
        print('Found nothing on best word, going to secondary')
        if "leastlongestword" in locals():
            for l2 in data:
                a2 = l2[0].split()
                if leastlongestword in a2:
                    data2.append(l2)
        else:
            return 'I dont know man...', f'```yaml\nERROR: All words in input where filtered out!```'

    print(f'database found {len(data2)} matches')

    if not data2:
        print(f'Found absolutley nothing...')
        return 'I dont know man...', f'```yaml\nERROR: No database matches!```'

    best = ("", "", 0.00)
    bestlist = []
    for l in data2:
        s = l[0]
        x = round(SequenceMatcher(a=i, b=s).ratio(), 2)
        if best[2] < x:
           best = (l[0], l[1], x)
           bestlist.append(best)
    bestlist.sort(key=lambda y: y[2])
    rpicked = random.choice(bestlist[-5:])

    print(f'{i} <-{rpicked[2]}-> {rpicked[0]}')
    sortdebugstuff = [i, rpicked[2], rpicked[0], len(data2),]

    debugstring = f'```yaml\nInput: {i}\n\n{len(data2)} potencial matches...\n{round(rpicked[2] * 100)}% matched with \nDatabase match: {rpicked[0]}\n\nOutput: {rpicked[1]}```'

    return rpicked[1], debugstring
