from difflib import SequenceMatcher
import time
import os

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
print(f'main database has {len(data)} entries.')


def rspeak(question):
    i = question
    longestword = i.split()
    xa = sorted(longestword, key=len)
    longestword1 = xa[-1]

    for l in data:
        a = l[0].split()
        if longestword1 in a:
            data2.append(l)

    print(f'database found {len(data2)} matches')

    start_time = time.time()
    best = ("", "", 0.00)
    for l in data2:
        s = l[0]
        x = round(SequenceMatcher(a=i, b=s).ratio(), 2)
        if best[2] < x:
           best = (l[0], l[1], x)
    print(f'completed in {round(time.time() - start_time, 4)}s')
    print(f'{i} <-{best[2]}-> {best[0]}')

    return(best[1])
