import random
import io

def random_line(fname):
    lines = open(fname, encoding='utf8').read().splitlines()
    x = random.choices(lines, k=10)
    return(x)

def get_speech(client):
    r = random_line('generalchat.txt')
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
