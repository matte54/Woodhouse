import json
import random

def pick_url():
    with open('data.json') as f:
        data = json.load(f)
        urls = []
    for i in data.keys():
        for e in data[i].keys():
            urls.append(e)

    picked = random.choice(urls)
    #maybe here add something that checks if "picked" is a v.reddit?
    return(picked)
