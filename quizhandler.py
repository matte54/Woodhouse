import os
import random
import json
from difflib import SequenceMatcher


class Quizhandler:
    def __init__(self):
        # on init walk quizdata folder and get all files
        self.quizfolder = "./quizdata/"
        for path, dirs, files in os.walk(self.quizfolder):
            pass
        if not files:
            print(f'no files found in quizdata/')

        self.scoredata, self.lifetimedata = self.loadscores()
        self.files = files
        self.limbo = []

    def loadscores(self):
        with open("./quizstats/score.json", "r") as scorefile:
            scoredata = json.load(scorefile)
        scorefile.close()
        with open("./quizstats/lifetime.json", "r") as lifetimefile:
            lifetimedata = json.load(lifetimefile)
        lifetimefile.close()
        return scoredata, lifetimedata

    def savescore(self, user, points):
        if user in self.scoredata:
            self.scoredata[user] += points
        else:
            self.scoredata[user] = points

        if user in self.lifetimedata:
            self.lifetimedata[user] += points
        else:
            self.lifetimedata[user] = points
        self.writescores()

    def writescores(self):
        with open("./quizstats/score.json", "w") as scorefile:
            json.dump(self.scoredata, scorefile, indent=4)
            scorefile.close()
        with open("./quizstats/lifetime.json", "w") as lifetimefile:
            json.dump(self.lifetimedata, lifetimefile, indent=4)
            lifetimefile.close()

    def resetscores(self):
        self.scoredata.clear()
        with open("./quizstats/score.json", "w") as scorefile:
            json.dump(self.scoredata, scorefile, indent=4)
            scorefile.close()
        print('Quiz scores reset')

    def listscores(self):
        scorestring = "----- current scores -----\n"
        with open("./quizstats/score.json", "r") as f:
            scoredata = json.load(f)
        f.close()
        if len(scoredata) != 0:
            sorted_scores = sorted(scoredata.items(), key=lambda x: x[1], reverse=True)
            for key, value in sorted_scores:
                scorestring += f'{key} - {value} points\n'
            return scorestring
        else:
            return "There is no scores to list"

    def listlifetime(self):
        scorestring = "----- lifetime scores -----\n"
        with open("./quizstats/lifetime.json", "r") as f:
            scoredata = json.load(f)
        f.close()
        if len(scoredata) != 0:
            sorted_scores = sorted(scoredata.items(), key=lambda x: x[1], reverse=True)
            for key, value in sorted_scores:
                scorestring += f'{key} - {value} points\n'
            return scorestring
        else:
            return "There is no lifetime scores to list"

    def getquestion(self, category):
        # needs a correct str of category
        categoryfiles = []
        questions = []
        invalid = False
        for f in self.files:
            if f.startswith(category):
                categoryfiles.append(f)
        for x in categoryfiles:
            with open(f'{self.quizfolder}{x}', 'r', encoding='UTF-8') as file:
                questions += file.read().splitlines()
        data = []
        for i in questions:
            i = i.lower()
            data.append((i.split(" / ")))
        datasize = len(data)
        for xi in range(datasize):
            pickedquestion = random.choice(data)
            if len(pickedquestion) != 3:
                invalid = True
                return pickedquestion, invalid
            qid = pickedquestion.pop(0)
            if qid not in self.limbo:
                self.limbo.append(qid)
                return pickedquestion, invalid  # returns q/a as list
        else:
            # cant rly think of any better solution then this for now
            print('Found no question not in limbo , fallback.')
            pickedquestion = random.choice(data)
            return pickedquestion  # returns q/a as list

    def getcategories(self):
        categorylist = []
        for f in self.files:
            categorylist.append(f[:-6])  # remove extension
        categorylist = list(dict.fromkeys(categorylist))
        return categorylist

    def answer(self, question, useranswer, username):
        # compare strings and return flare + % of answer likeness
        ratio = SequenceMatcher(a=question[1], b=useranswer).ratio()
        ratio = round(ratio * 100)
        if ratio == 100:
            points = 5
        elif ratio >= 90:
            points = 3
        elif ratio >= 50:
            points = 1
        else:
            points = 0
        self.savescore(username, points)
        return ratio, points
