import json
import random

def pick_url():
    with open('data.json') as f:
        data = json.load(f)
        urls = []
    for i in data.keys():
        for e in data[i].keys():
            link = data[i][e]["dlink"]
            # check if post is a reddit video
            if link.startswith("https://v.redd.it"):
                link = data[i][e]["link"]
            urls.append(link)

    picked = random.choice(urls)
    return(picked)
