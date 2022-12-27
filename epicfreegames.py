from epicstore_api import EpicGamesStoreAPI
import requests
import datetime

DEBUG = True  # turn off for live
hc_url = "https://store.epicgames.com/en-US/p/"


def filter_steam_games():
    gamesalelist = []
    url = "http://store.steampowered.com/api/featuredcategories/?l=english"
    res = requests.get(url)
    saledict = dict(res.json())

    for i in saledict["specials"]["items"]:
        if i["discount_percent"] > 40:
            gamesalelist.append(i)

    # check ids
    with open('./data/freegames.txt') as id_f:
        id_database = id_f.read().splitlines()
    for games in gamesalelist:
        if games["id"] in id_database:
            if DEBUG:
                print(f'found dupe {games["id"]}')
            gamesalelist.remove(games)

    if gamesalelist:
        f = open('./data/freegames.txt', "a")
        for game in gamesalelist:
            f.write(game["id"] + "\n")
        f.close()

    msgformat = f'{i["name"]} {i["discount_percent"]}% sale price {i["final_price"]} EUR until {datetime.datetime.fromtimestamp(i["discount_expiration"])}'

def filter_epic_games(gamelist, current_free_dicts):
    for x in gamelist:
        current_free_dicts.append(x)

    for i in current_free_dicts:
        if i["productSlug"] == "[]":
            current_free_dicts.remove(i)
            if DEBUG:
                print(f'ignoring "{i["title"]}" not a game.')

    # check for already seen game
    with open('./data/freegames.txt') as id_f:
        id_database = id_f.read().splitlines()
    for games in current_free_dicts:
        if games["id"] in id_database:
            if DEBUG:
                print(f'found dupe {games["id"]}')
            current_free_dicts.remove(games)
    return current_free_dicts


def gatherepic_gamedata(current_free_dicts):
    if len(current_free_dicts) > 0:
        if DEBUG:
            print("theres stuff in the list")
            print(current_free_dicts)
        f = open('./data/freegames.txt', "a")
        for game in current_free_dicts:
            f.write(f'{game["id"]}\n')
        f.close()
        return True, current_free_dicts

    else:
        if DEBUG:
            print("No new free games, doing nothing.")
        return False, current_free_dicts



def getfreegames():
    api = EpicGamesStoreAPI()
    free = api.get_free_games()
    gamelist = free["data"]["Catalog"]["searchStore"]["elements"]
    current_free_dicts = []
    msg_list = []

    # epic games stuff
    thedict = filter_epic_games(gamelist, current_free_dicts)
    b, end_current_free_dicts = gatherepic_gamedata(thedict)
    if DEBUG:
        print(f'dict contains {end_current_free_dicts}')
    if b:
        if DEBUG:
            print(f'Creating post message!')
        for i in end_current_free_dicts:
            end = i["promotions"]["promotionalOffers"][0]
            end2 = end["promotionalOffers"][0]
            end3 = end2["endDate"]
            msg = f'FREE GAME! UNTIL {end3}\n {hc_url}{i["productSlug"]}'
            msg_list.append(msg)
            if DEBUG:
                print(f'Msg list contains: {msg}')

    # steam stuff here eventually

    if len(msg_list) > 0:
        if DEBUG:
            print('f Returning msg_list to main file')
        return msg_list  # return list of games to send
