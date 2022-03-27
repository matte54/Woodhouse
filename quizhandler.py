import os
import random
from difflib import SequenceMatcher


class Quizhandler:
    def __init__(self):
        # on init walk quizdata folder and get all files
        self.quizfolder = "./quizdata/"
        for path, dirs, files in os.walk(self.quizfolder):
            pass
        if not files:
            print(f'no files found in quizdata/')
        self.files = files

    def getquestion(self, category):
        # needs a correct str of category
        categoryfiles = []
        questions = []
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
        pickedquestion = random.choice(data)
        return pickedquestion  # returns q/a as list

    def getcategories(self):
        categorylist = []
        for f in self.files:
            categorylist.append(f[:-6])  # remove extension
        categorylist = list(dict.fromkeys(categorylist))
        return categorylist

    def answer(self, question, useranswer):
        # compare strings and return flare + % of answer likeness
        ratio = SequenceMatcher(a=question[1], b=useranswer).ratio()
        ratio = round(ratio * 100)
        if ratio == 100:
            flare = "CORRECT!"
        elif ratio >= 90:
            flare = "RIGHT!"
        elif ratio >= 50:
            flare = "Close..."
        else:
            flare = "Wrong"
        return flare, ratio
