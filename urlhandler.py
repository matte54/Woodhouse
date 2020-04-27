import json
import random

def pick_url():
    with open('data.json') as json_file:
        data = json.load(json_file)
        urls = []
        for i in data['https://www.reddit.com/r/gifs/.rss']:
            x = data['https://www.reddit.com/r/gifs/.rss'][i]['dlink']
            urls.append(x)

        for i in data['https://www.reddit.com/hot/.rss']:
            x = data['https://www.reddit.com/hot/.rss'][i]['dlink']
            urls.append(x)

        for i in data['https://www.rockpapershotgun.com/feed/']:
            x = data['https://www.rockpapershotgun.com/feed/'][i]['link']
            urls.append(x)

        for i in data['https://www.gamespot.com/feeds/news/']:
            x = data['https://www.gamespot.com/feeds/news/'][i]['link']
            urls.append(x)

        picked = random.choice(urls)
        return(picked)
