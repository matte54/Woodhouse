import random
import io
import markovify
import requests
from lxml import etree as ET

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
    for l in range(10):
        r.append(text_model.make_sentence())
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
