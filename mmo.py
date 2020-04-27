import random
import math
import csv
import operator
import pandas as pd

# def gameStart():
#     x = input("Enter player name:")
#     i = input("Enter your class:")
#     return x,i

def highscore():
    result = pd.read_csv('highscore.txt')
    unsorted_df = pd.DataFrame(result)
    sorted_df = unsorted_df.sort_values(by=['Level','ItemLvl'],ascending=False).head(11)
    fHighscore = sorted_df.to_string(index = False)
    x = "```<-------------------- HIGHSCORE -------------------->\n"
    z = "\n<-------------------- HIGHSCORE -------------------->```"
    scoreReturn = x+fHighscore+z
    return(scoreReturn)



#playerName, className = gameStart()

def playMMO(playerName, className):
    player = True
    playerLevel = 1.0
    playerGearLvl = 0.0
    fights = 0
    xp = 0.0
    xpRoof = 8.0
    powerCreep = 0.0
    EZROLL = 1.0

    #weapons
    First = ['Powerful', 'Weak', 'Steel', 'Wooden', 'Flaming', '', 'Cold', 'Magic', 'Heavy', 'Light', 'Bronze', 'Gold', 'Elven', 'Spiked', 'Crude', 'Strong', 'Rusty', 'Kings', 'Soldiers', 'Warlocks', 'Mages', 'Thiefs', 'Rogues', 'Lords', 'Queens', 'Princes']
    Second = ['Sword', 'Staff', 'Mace', 'Staff', 'Rod', 'Knife', 'Dagger', 'Claymore', 'Pitchfork', 'Shortsword', 'Cutlass', 'Gladius', 'Sabre', 'Sickle', 'Broadsword', 'Axe', 'Hammer', 'Morningstar', 'Club', 'Scepter', 'Trident', 'Spear', 'Bow', 'Crossbow', 'Longbow', 'Polearm', 'Pike', 'Gauntlet', 'Poleaxe']
    Third = ['Fire', 'The Grand Master', 'Ruin', 'The Wraith', 'The Cold', 'The Vampire', 'Doom', 'Weakness', 'Crippling', 'Haste', 'Slow', 'Light', 'Darkness', 'Dark', 'Wind', 'Swiftness', 'The Crow', 'The Orc', 'The Mage', 'The Warrior', 'The Rogue', 'The Warlock', 'Ice', 'Earth', 'The Lost', 'Hell', 'Heaven']
    xW = random.choice(First)
    yW = random.choice(Second)
    zW = random.choice(Third)
    rW = bool(random.getrandbits(1))
    if rW == True:
        selectedWeapon = "{} {} of {}".format(xW,yW,zW)
    else:
        selectedWeapon = "{} {}".format(xW,yW)

    monsters = ['Orc', 'Dragon', 'Human', 'Trap', 'Goblin', 'Golem', 'Vampire', 'Flumph', 'Mimic', 'Modron', 'Drider', 'Rust Monster', 'Troll', 'Wraith', 'Gnoll', 'Lich', 'Beholder', 'Gelatinous Cube', 'Githyanki', 'Illithid', 'Slaad', 'Owlbear', 'Displacer Beast', 'Tarrasque', 'Kobold', 'Skeleton', 'Duckbunny', 'Prismatic Dragon']
    flavor = ['Your valor will be remembered...', 'His/Her courage was admirable...', 'R.I.P', 'Rest in pepperonis...', 'Watch out for those claws...']

    while player == True:
        rDif = random.uniform(0.0,2.0)+powerCreep #random diffculty roll
        mDif = random.uniform(-1.0,1.0) #monster diffculty roll
        fDif = playerLevel+rDif+mDif-playerGearLvl #final diffculty
        #print("Fight diffculty number was:{}".format(round(fDif,2)))

        playerRoll = random.uniform(1.0,6.0)
        if playerLevel < 5.0:
            playerFinalRoll = playerRoll+playerLevel+EZROLL
        else:
            playerFinalRoll = playerRoll+playerLevel
        #print("The players final roll was {}".format(round(playerFinalRoll,2)))

        if playerFinalRoll >= fDif:
            fights += 1
            if mDif < 0.0:
                fightXp = playerLevel
            else:
                fightXp = playerLevel+mDif
            xp = xp+fightXp
            #print("Experience gained was {}".format(round(fightXp,2)))

            if xp >= xpRoof:
                playerLevel += 1.0
                xpRoof += 2.0
                xp = 0.0
                if playerLevel > 6.0:
                    powerCreep += 0.25
                #print("DING {}!".format(int(playerLevel)))

            if random.randint(1,10) > 8:
                foundGear = random.uniform(0.01,0.5)
                playerGearLvl = playerGearLvl+foundGear
                #print("Found an item worth + {} item level".format(round(foundGear,2)))

            if fights == 300:
                player = False

        else:
            player = False

    deathILevel = round(playerGearLvl, 2)
    deathDiff = round(fDif, 2)
    deathRoll = round(playerFinalRoll, 2)
    deathLevel = int(playerLevel)
    deathMonsterLevel = round(playerLevel+mDif)
    deathMonster = random.choice(monsters)
    pFlavor = random.choice(flavor)
    deathXp = round(xp, 2)
    line1 = "```{} the {} died , {}\n".format(playerName, className, pFlavor)
    line2 = "Your level was {}, you survived {} encounters\n".format(deathLevel, fights)
    line3 = "Your chosen weapon was: {}, and your gear level was {}\n".format(selectedWeapon, deathILevel)
    line4 = "Your demise came from a lvl {} {}, your foe rolled {} and your roll was only {}\n".format(deathMonsterLevel, deathMonster, deathDiff, deathRoll)
    line5 = "Your experience was {}/{}```".format(deathXp, xpRoof)
    endscreen = line1+line2+line3+line4+line5
    playerData = [[playerName, className, deathLevel, fights, deathILevel]]

    f = open('highscore.txt', 'a')
    with f:
        writer = csv.writer(f)
        writer.writerows(playerData)
    f.close()
    return(endscreen)
