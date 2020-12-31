import discord
import logging
import os
import re
import io
import random
import asyncio
import credentials
import socket
import hashlib
from discord.ext import tasks, commands
from urlhandler import pick_url
from mmo import playMMO
from mmo import highscore
from pokemon import spawn_pokemon
from pokemon import find_pokemon_sprite
import csv
import pandas as pd
import time
from mainfunc import get_speech, ranswer, get_holiday
from spider_silk import db, Post

DEBUG = False
if hashlib.md5(socket.gethostname().encode('utf-8')).hexdigest() == '18093712d226974bfc25563025ebdb3c':
    DEBUG = True

try:
    TOKEN = credentials.KEY
except AttributeError:
    print('Ignoring credentials key...')

if DEBUG:
    with open('catmaker', encoding='utf-8') as f:
        TOKEN = f.read()

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

#Flare?
response_flare = ["you talking to me?", "what was that?", "uhm...", "suuuure...", "Thats my name dont wear it out", "Oh hey!", "whats up?"]

# Badges constants
THRESHOLDS = [111 * n + 6 for n in range(1, 9)] # 8 badges
BADGE_PATH_SINGLE = [f'badges/Badge{n}.png' for n in range(1, 9)] # individual badge icons
BADGE_PATH_PROGRESS = [f'badges/Badge{n}a.png' for n in range(1, 9)] # cumulative badges


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
                        g = random.randint(1, 100)
                        if g < 75:
                            t = get_timestamp_str()
                            x = get_speech(self)
                            print('{}Automatic trigger chosen reply was -----> {}'.format(t, x))
                            await message.channel.send(x)
                            counter = 0
                        else:
                            t = get_timestamp_str()
                            x = get_holiday()
                            print('{}Holiday weirdness -----> {}'.format(t, x))
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

        if message.author != self.user:
            #message mentions woodhouse with or with caps?
            if message.content.__contains__("Woodhouse") or message.content.__contains__("woodhouse"):
                t = get_timestamp_str()
                u = message.author
                u_str = str(u)[:-5]
                #TODO move this get_speech call to where its needed to improve response time
                i = get_speech(self)
                p = bool(random.getrandbits(1))
                if p == True:
                    await message.channel.send(i)
                    print('{} {} mentioned woodhouse by name , response was -----> {}'.format(t, u, i))
                else:
                    o = bool(random.getrandbits(1))
                    if o == True:
                        i2 = random.choice(response_flare)
                        c_response = u_str + ", " + i2
                        await message.channel.send(c_response)
                        print('{} {} mentioned woodhouse by name , response was -----> {}'.format(t, u, c_response))
                    else:
                        b_response = i + ", " + u_str
                        await message.channel.send(b_response)
                        print('{} {} mentioned woodhouse by name , response was -----> {}'.format(t, u, b_response))
                break
        break


        if message.content.startswith('$url'):
            i = pick_url()
            t = get_timestamp_str()
            u = message.author
            print('{}Manual triggered URL request by {} -----> {}'.format(t, u, i))
            await message.channel.send(i)

        if message.content.startswith('$holiday'):
            i = get_holiday()
            t = get_timestamp_str()
            u = message.author
            print('{}Manual triggered Holiday request by {} -----> {}'.format(t, u, i))
            await message.channel.send(i)

        m = re.search(r'(?:\s|^)(\-?\d+)( ?celcius| ?fahrenheit|c|f)\b', txt, flags=re.IGNORECASE)
        if m:
            t = get_timestamp_str()
            u = message.author
            i = int(m[1])
            unit = m[2]
            if unit.lower().startswith('c'):
                c = round(9.0/5.0 * i + 32)
                resp = ['Muuuurica!', '', 'Sir, ', 'I know what that is in freedom units']
                r = random.choice(resp)
                msg = f'{r} {i}c is {c}f'
                print(f'{t} Converted C to F for {u}')
                await message.channel.send(msg)
            if unit.lower().startswith('f'):
                c = round((i - 32) * 5.0/9.0)
                resp = ['Sir im delighted to tell you that', '', 'Sir, ', 'Oh oh oh! i know that',
                        'My superior intelligence tell me that']
                r = random.choice(resp)
                msg = f'{r} {i}f is {c}c'
                print(f'{t} Converted F to C for {u}')
                await message.channel.send(msg)
        break

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
            #x = get_speech(self)
            x = ranswer() #Testing markovify
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

            with open(filePathDex) as f2:
                # list of mons stripping newlines and removing empty lines
                mons = [mon.strip() for mon in f2.readlines() if mon.strip()]
                count = len(mons)
                badge_num = -1
                if count >= THRESHOLDS[0]:
                    badge_num = 0
                    while count >= THRESHOLDS[badge_num + 1]:
                        badge_num += 1
                # badge_text = '' if badge_num < 0 else f'{badge_num + 1}/8 BADGES'
                # status = f'{dexUser}\'s POKÉDEX  {count}/894 CAUGHT  {badge_text}'
                # last_five = '\n'.join(mons[-5:])
                # if count == 0: last_five = '  GO CATCH SOME POKÉMON FIRST'
                trainer = str(dexUser).replace('#', '%23')
                url = f'http://thedarkzone.se/arachne/pokedex?trainer={trainer}'
                # msg = f'```{status}\n{last_five}```\n{url}'

                # TODO embed user's arachne avatar?
                embed = discord.Embed()
                embed.title = f'{dexUser}\s POKÉDEX'
                embed.url = url
                last_five = '\n'.join(['> ' + mon for mon in mons[-5:]])
                if count == 0:
                    last_five = 'Go catch some pokémon first!'
                embed.add_field(name='CAUGHT', value=f'{count}/894', inline=True)
                if badge_num >= 0:
                    embed.add_field(name='BADGES', value=f'{badge_num + 1}/8', inline=True)
                embed.add_field(name='Last 5 Pokémon', value=last_five, inline=False)

                if badge_num >= 0:
                    await message.channel.send(embed=embed, file=discord.File(BADGE_PATH_PROGRESS[badge_num]))
                else:
                    await message.channel.send(embed=embed)


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
                            msg = f'yaml\n{discordId} CAUGHT {pokePick}!'
                            badge_pic = None
                            if count in THRESHOLDS:
                                badge_num = THRESHOLDS.index(count)
                                badge_pic = BADGE_PATH_SINGLE[badge_num]
                                msg += f'\n {discordId} EARNED A NEW BADGE!'
                                await message.channel.send(f'```{msg}```', file=discord.File(badge_pic))
                            else:
                                await message.channel.send(f'```{msg}```')
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
                            await message.channel.send("""```yaml\n{} CAUGHT {}...but already had it!```""".format(discordId, pokePick))
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
