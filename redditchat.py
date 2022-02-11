from difflib import SequenceMatcher
import time
import os
import random

texte = ""
logfolderpath = "./rdata/"
for path, dirs, files in os.walk(logfolderpath):
    pass
for e in files:
    with open(f'./rdata/{e}', 'r' , encoding='UTF-8') as f:
        texte += f.read()

text = texte.splitlines()

data = []
data2 = []
for i in text:
    data.append((i.split(" / ")))
#print(f'main database has {len(data)} entries.')


def rspeak(question):
    i = question
    longestword = i.split()
    xa = sorted(longestword, key=len)
    longestword1 = xa[-1]
    if len(xa) >= 2:
        leastlongestword = xa[-2]

    for l in data:
        a = l[0].split()
        if longestword1 in a:
            data2.append(l)

    #check the next least longestword?
    if not data2:
        for l in data:
            a = l[0].split()
            if leastlongestword in a:
                data2.append(l)

    #last ditch effort if not finding anything
    if not data2:
        return('I dont know man...')

    print(f'database found {len(data2)} matches')

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

    return(rpicked[1])
