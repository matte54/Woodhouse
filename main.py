import discord
import logging
import os
import re
import io
import random
import asyncio
import credentials
from discord.ext import tasks, commands
from urlhandler import pick_url
from mmo import playMMO
from mmo import highscore
from pokemon import spawn_pokemon
from pokemon import find_pokemon_sprite
import csv
import pandas as pd
import time
from mainfunc import get_speech
from spider_silk import db, Post

TOKEN = credentials.KEY

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Heroin addict')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

global pokemonAlive
global shutup
shutup = 0


# Badges constants
THRESHOLDS = [111 * n + 6 for n in range(1, 9)] # 8 badges
BADGE_PATH_SINGLE = [f'badges/Badge{n}.png' for n in range(1, 9)] # individual badge icons
BADGE_PATH_PROGRESS = ['badges/Badge1.png'] + [f'badges/Badge{n}a.png' for n in range(2, 9)] # cumulative badges


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())
        self.bg_task = self.loop.create_task(self.pokemon_task())

    async def on_ready(self):
        t = get_timestamp_str()
        x = 'Logged in as'
        y = self.user.name
        z = self.user.id
        print ('{}{} {} id {} - READY'.format(t, x, y, z))

    async def on_disconnect(self):
        t = get_timestamp_str()
        print('{}Connection LOST to discord servers!'.format(t))

    async def on_connect(self):
        t = get_timestamp_str()
        print('{}Connection ESTABLISHED to discord servers!'.format(t))

    async def on_resumed(self):
        t = get_timestamp_str()
        print('{}Connection resumed?'.format(t))

    async def pokemon_task(self):
        global pokemonAlive
        global shutup
        pokemonAlive = 0
        await self.wait_until_ready()
        channel = self.get_channel(194028816333537280) # channel ID goes here
        while not self.is_closed():
            await asyncio.sleep(7000)
            if shutup == 1:
                t = get_timestamp_str()
                print('{}Shutup function is ON waiting 6 hours...'.format(t))
                await asyncio.sleep(21600)
                shutup = 0
            async for message in channel.history(limit=1):
                if message.author == self.user:
                    t = get_timestamp_str()
                    print('{}Last message was me, avoiding spam no pokemon now...'.format(t))
                    dexR = random.randint(60, 120)
                    await asyncio.sleep(dexR)
                elif pokemonAlive == 0:
                    pokemonAlive = 1
                    t = get_timestamp_str()
                    print('{}Spawning pokemon now...'.format(t))
                    global pokePick
                    pokePick = spawn_pokemon()
                    pokePic = find_pokemon_sprite(pokePick)
                    if len(pokePic) > 9:
                        await message.channel.send('', file=discord.File(pokePic))
                    pokePickLine = """```yaml\nA WILD {} APPEARED!```""".format(pokePick)
                    await message.channel.send(pokePickLine)
                    await asyncio.sleep(600)
                    if pokemonAlive == 1:
                        pokemonAlive = 0
                        pokemonRun = """```yaml\n{} RAN AWAY!```""".format(pokePick)
                        await message.channel.send(pokemonRun)

                else:
                    dexR2 = random.randint(1200, 1800)
                    await asyncio.sleep(dexR2)

    async def my_background_task(self):
        global shutup
        counter = 0
        await self.wait_until_ready()
        channel = self.get_channel(194028816333537280) # channel ID goes here
        while not self.is_closed():
            await asyncio.sleep(30)
            if shutup == 1:
                t = get_timestamp_str()
                print('{}Shutup function is ON waiting 6 hours...'.format(t))
                await asyncio.sleep(21600)
                shutup = 0

            async for message in channel.history(limit=1):
                if message.author == self.user:
                    counter +=1
                    t = get_timestamp_str()
                    print('{}Last message was me, waiting... i have waited {} cycle(s).'.format(t, counter))
                    pass
                else:
                    i = random.randint(1, 100)
                    t = get_timestamp_str()
                    print('{}0-100 Roll came up {}'.format(t, i))
                    if i > 70 :
                        t = get_timestamp_str()
                        x = get_speech(self)
                        print('{}Automatic trigger chosen reply was -----> {}'.format(t, x))
                        await message.channel.send(x)
                        counter = 0
                    elif i < 15:
                        z = pick_url()
                        t = get_timestamp_str()
                        print('{}URL post triggered -----> {}'.format(t, z))
                        await message.channel.send(z)
                        x = get_speech(self)
                        t = get_timestamp_str()
                        print('{}Automatic trigger chosen reply was -----> {}'.format(t, x))
                        await message.channel.send(x)
                        print("-----------------------")
                        counter = 0

                    else:
                        counter += 1
                        t = get_timestamp_str()
                        print('{}Can post but waiting...i have waited {} cycle(s)'.format(t, counter))
                        pass
            x = random.randint(4000, 7000)
            await asyncio.sleep(x)

    async def on_message(self, message):
        txt = message.content

        if message.author == self.user:
            #print("It was me!")
            return

        if message.content.startswith('$url'):
            i = pick_url()
            t = get_timestamp_str()
            u = message.author
            print('{}Manual triggered URL request by {} -----> {}'.format(t, u, i))
            await message.channel.send(i)

        if re.search(r'[0-9]{1,3}[Ff]\b', txt):
            t = get_timestamp_str()
            u = message.author
            i = re.search(r'[0-9]{1,3}[Ff]\b', txt)
            i = i.group(0)[:-1]
            i = int(i)
            c = round((i - 32) * 5.0/9.0)
            resp = ['Sir im delighted to tell you that', '', 'Sir, ', 'Oh oh oh! i know that', 'My superior intelligence tell me that']
            r = random.choice(resp)
            x = '{} {}f is {}c'.format(r, i, c)
            print('{} Converted F to C for {}'.format(t, u))
            await message.channel.send(x)

        if re.search(r'[0-9]{1,3}[Cc]\b', txt):
            t = get_timestamp_str()
            u = message.author
            i = re.search(r'[0-9]{1,3}[Cc]\b', txt)
            i = i.group(0)[:-1]
            i = int(i)
            c = round(9.0/5.0 * i + 32)
            resp = ['Muuuurica!', '', 'Sir, ', 'I know what that is in freedom units']
            r = random.choice(resp)
            x = '{} {}c is {}f'.format(r, i, c)
            print('{} Converted C to F for {}'.format(t, u))
            await message.channel.send(x)

        if message.content.startswith('$highscore'):
            x = highscore()
            t = get_timestamp_str()
            u = message.author
            print('{}{}Requested highscore list....'.format(t, u))
            await message.channel.send(x)

        if message.content.startswith('$shutup'):
            global shutup
            if shutup == 0:
                shutup = 1
                t = get_timestamp_str()
                u = message.author
                print('{}{} Told woodhouse to shutup...'.format(t, u))
                l = ['Yes, sir.', 'righto', 'Its gonna be a itchy day...', 'will do!', 'Very good, sir.']
                x = random.choice(l)
                await message.channel.send(x)
            else:
                t = get_timestamp_str()
                u = message.author
                print('{}{} Told woodhouse to shutup...but he was already doing it.'.format(t, u))
                k = str(u)
                y = k[:-5]
                x = '{} im terribly sorry but i cant shut up more then i already am...'.format(y)
                await message.channel.send(x)


        if message.content.startswith('$speak'):
            x = get_speech(self)
            t = get_timestamp_str()
            u = message.author
            print('{}Manual trigger issued by {} chosen reply was -----> {}'.format(t, u, x))
            await message.channel.send(x)

        if message.content.startswith('$test'):
            count = 0
            seek = 10
            channel = self.get_channel(194028816333537280)
            async for message in channel.history(limit=seek):
                if message.author == self.user:
                    count +=1
            print('{}/{} of the last messages was Woodhouses...'.format(count, seek))

        if message.content.startswith('$dex'):
            dexUser = message.author
            t = get_timestamp_str()
            print('{}Listing {}s pokédex...'.format(t, dexUser))
            uiDex = str(dexUser)
            filePathDex = './data/'+uiDex
            fE = open(filePathDex, 'a')
            fE.close()

            with open(filePathDex) as f:
                content = f.readlines()
                list2 = [a for a in content if a != '\n']
                list3 = [i.strip() for i in list2]
                c = len(list3)
                test1 = ""
                for name in list3:
                    test1 += name.ljust(15)
                x = "```{} POKÈDEX\n".format(dexUser)
                z = "\n{}/896 CAUGHT```".format(c)
                ccDex = x+test1+z
                badge_pic = None
                if c > THRESHOLDS[0]:   # If we have at least 1 badge, show all the badges we have
                    i = 0
                    while c < THRESHOLDS[i]:
                        i += 1
                    badge_num = i
                    badge_pic = BADGE_PATH_PROGRESS[badge_num]
                
                if len(test1) < 1800:
                    if badge_pic:
                        await message.channel.send(ccDex, file=badge_pic)
                    else:
                        await message.channel.send(ccDex)
                else:
                    ccDexTemp = x+"To many mons caught, working on it..."+z
                    if badge_pic:
                        await message.channel.send(ccDexTemp, file=badge_pic)
                    else:
                        await message.channel.send(ccDexTemp)


        if message.content.startswith('$catch'):
            global pokemonAlive
            global pokePick
            discordId = message.author
            discordName = message.author.name #test
            t = get_timestamp_str()
            print('{}{} is attempting pokemon catch...'.format(t, discordId))
            uid = str(discordId)
            if pokemonAlive == 1:
                #catchAttempt = bool(random.getrandbits(1))
                if random.randint(1,10) < 9:
                    pokemonAlive = 0
                    filePath = './data/'+uid
                    f = open(filePath, 'a')
                    # fE = open(filePath, 'w+')
                    # fE.close()
                    record = pokePick.title()
                    recordEntry = [record]

                    with open(filePath) as fDex2:
                        contentDex = fDex2.readlines()
                        listC2 = [a for a in contentDex if a != '\n']
                        listC3 = [i.strip() for i in listC2]
                        #print(listC3)
                        listC4 = ('\n'.join(map(str, listC3)))

                        if record not in listC4:
                            count = len(listC4.split('\n')) + 1 # Use this to figure out if a player has reached a badge
                            #f = open(filePath, 'a')
                            writer = csv.writer(f)
                            writer.writerow(recordEntry)
                            f.close()
                            message = f'yaml\n{discordId} CAUGHT {pokePick}!'
                            badge_pic = None
                            if count in THRESHOLDS:
                                badge_num = THRESHOLDS.index(count)
                                badge_pic = BADGE_PATH_SINGLE[badge_num]
                                message += f'\n {discordId} EARNED A NEW BADGE!'
                                await message.channel.send(f'```{message}```', file=badge_pic)
                            else:
                                await message.channel.send(f'```{message}```')
                            t = get_timestamp_str()
                            print('{}{} caught {}'.format(t, discordId, pokePick))
                            #Catch history entry
                            try:
                                postCatch = Post(body='{} CAUGHT {}!'.format(discordName, pokePick), pokemon=pokePick, user_id=discordId.id)
                                db.session.add(postCatch)
                                db.session.commit()
                            except Exception as e:
                                print('{}ERROR Could not put pokemon into catch history!'.format(t))
                                print(e)
                        else:
                            await message.channel.send("""```yaml\n{} CAUGHT {}...but he/she already had it!```""".format(discordId, pokePick))
                            #print("We had that one...")

                else:
                    await message.channel.send("""```yaml\n{} BROKE OUT FOR {}!```""".format(pokePick, discordId))

        if message.content.startswith('$mmo'):
            mmoMessage = message.content.replace('$mmo ','')
            if len(mmoMessage.split()) != 2:
                print('Wrong string input')
                return
            mmoName, mmoClass = mmoMessage.split(' ', 1)
            mmoScore = playMMO(mmoName, mmoClass)
            t = get_timestamp_str()
            u = message.author
            print('{}{} played the mmo...'.format(t, u))
            await message.channel.send(mmoScore)


def get_timestamp_str():
    i = time.strftime("%H:%M:%S - ")
    return(i)

client = MyClient()
client.run(TOKEN)
