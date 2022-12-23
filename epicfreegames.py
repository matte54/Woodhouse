from epicstore_api import EpicGamesStoreAPI

DEBUG = False  # turn off for live

api = EpicGamesStoreAPI()
free = api.get_free_games()
gamelist = free["data"]["Catalog"]["searchStore"]["elements"]
current_free_dicts = []
msg_list = []
hc_url = "https://store.epicgames.com/en-US/p/"


def filter_games():
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
    id_f.close()


def gathergamedata():
    if len(current_free_dicts) > 0:
        if DEBUG:
            print("theres stuff in the list")
            print(current_free_dicts)
        f = open('./data/freegames.txt', "a+")
        for game in current_free_dicts:
            f.write(game["id"]+"\n")
        f.close()
        return True

    else:
        if DEBUG:
            print("No new free games, doing nothing.")
        return False


def getfreegames():
    filter_games()
    b = gathergamedata()
    if b:
        for i in current_free_dicts:
            end = i["promotions"]["promotionalOffers"][0]
            end2 = end["promotionalOffers"][0]
            end3 = end2["endDate"]
            msg = f'FREE GAME! UNTIL {end3}\n {hc_url}{i["productSlug"]}'
            msg_list.append(msg)

        for x in msg_list:
            print(x)
        return msg_list  # return list of games to send
