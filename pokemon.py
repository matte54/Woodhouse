import random
import json
import pandas as pd
import glob


def spawn_pokemon():
    df = pd.read_csv('pokemons.txt')
    elements = df.sample()
    moop = elements.to_string(index = False, header = False)
    moop2 = moop.lstrip()
    moop3 = moop2.upper()

    return(moop3)

def find_pokemon_sprite(text):
    lowercasestring = text.lower()
    dir = ("./mons/")
    wildcard = ("*.png")
    finalstring = dir+lowercasestring+wildcard
    files = glob.glob(finalstring)
    extractedstring = (files[0])
    s = list(extractedstring)
    s[6] = '/'
    x = "".join(s)

    return(x)

#find_pokemon_sprite()
