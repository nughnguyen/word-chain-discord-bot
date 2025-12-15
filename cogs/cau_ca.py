
from random import *
from time import sleep
print('Type \'fish\' and press enter to start fishing. Type \'help\' for help.')

global fishies, salmon, cod, tropicalFish, pufferfish, fieryPufferfish, volcanicFish, turtle, squid, dolphin
fishies = 0
salmon = 0
cod = 0
tropicalFish = 0
pufferfish = 0
fieryPufferfish = 0
volcanicFish = 0
turtle = 0
squid = 0
dolphin = 0

global money
money = 0

global quantity, quality, treasure, multi, betterfish, morefish, salesmen, boost, exotic, bait, beat_game, boostbooster, treasurehoarder, baitlover, xp, level, xm, upgrader
quantity = 1
quality = 1.1
treasure = 1
multi = 1
betterfish = 0
morefish = 0
salesmen = 0
fishboost = 0
catchboost = 0
treasureboost = 0
exotic = 0
bait = 0
current_bait = 0
baitlover = 1
treasurehoarder = 1
boostbooster = 1
xp = 0
xm = 1
xpnext = 35
level = 1
upgrader = 0
beat_game = False

fish_xp_values = {
    'Fish': 0.25,
    'Salmon': 1,
    'Cod': 2,
    'Tropical Fish': 5,
    'Pufferfish': 10,
    'Fiery Pufferfish': 20,
    'Volcanic Fish': 40,
    'Turtle': 75,
    'Squid': 120,
    'Dolphin': 150
}


def fish(quik):
    global fishboost, catchboost, treasureboost, exotic, beat_game, bait, boostbooster, treasurehoarder, baitlover, xp, fish_type, newXP, level, xm


    fishover = False
    catchover = False
    treasureover = False
    
    newFish = 0
    newSalmon = 0
    newCod = 0
    newTropicalFish = 0
    newPufferfish = 0
    newFieryPufferfish = 0
    newVolcanicFish = 0
    newTurtle = 0
    newSquid = 0
    newDolphin = 0
    newExotic = 0
    newXP = 0 

    newQuality = quality
    newQuantity = quantity
    newTreasure = treasure

    baitover = False

    if current_rod == 'Plastic Rod':
        newQuantity *= 1.1
        newQuality += 0.3
    if current_rod == 'Improved Rod':
        newQuantity *= 1.15
        newQuality += 0.6
    if current_rod == 'Greater Rod':
        newQuantity *= 1.25
        newQuality += 1
    if current_rod == 'Fiberglass Rod':
        newQuantity *= 1.35
        newQuality += 1.4
    if current_rod == 'Lava Rod':
        newQuantity *= 1.5
        newQuality += 1.7
    if current_rod == 'Magma Rod':
        newQuantity *= 1.75
        newQuality += 2.0
    if current_rod == 'Oceanic Rod':
        newQuantity *= 2
        newQuality += 2.3
    if current_rod == 'Aquatic Rod':
        newQuantity *= 2.5
        newQuality += 2.6
    if current_rod == 'Golden Rod':
        newQuantity *= 3
        newQuality += 3
    if current_rod == 'Treasure Rod':
        newTreasure *= 2


    # Add boat enhancements
    if current_boat == 'Canoe':
        newQuality += 0.15
        newTreasure *= 1.1
    elif current_boat == 'Sailboat':
        newQuality += 0.3
        newTreasure *= 1.2
    elif current_boat == 'Motor Boat':
        newQuality += 0.45
        newTreasure *= 1.3
    elif current_boat == 'Speed Boat':
        newQuality += 0.6
        newTreasure *= 1.4
    elif current_boat == 'Catamaran':
        newQuality += 0.75
        newTreasure *= 1.5
    elif current_boat == 'Pontoon':
        newQuality += 0.9
        newTreasure *= 1.6
    elif current_boat == 'Ship':
        newQuality += 1.05
        newTreasure *= 1.7
    elif current_boat == 'Fishing Boat':
        newQuality += 1.2
        newTreasure *= 1.8
    elif current_boat == 'Cruise':
        newQuality += 1.5
        newTreasure *= 2.0

    
        
    if fishboost > 0:
        fishboost -= 1
        newQuantity *= (1.5 * boostbooster) 
    if catchboost > 0:
        catchboost -= 1
        newQuality += (0.5 * boostbooster)
    if treasureboost > 0:
        if quik == 'no':
                treasureboost -= 1
                newTreasure *= (1.5 * boostbooster) 

    if fishboost == 1:
        fishover = True
    if catchboost == 1:
        catchover = True
    if treasureboost == 1:
        treasureover = True

    if bait == 1:
        baitover = True

    if bait > 0:
        if current_bait == 'Worms':
            newQuantity *= (1.4 * baitlover)
        if current_bait == 'Leeches':
            newQuantity *= (1.25 * baitlover)
            newQuality += (0.4 * baitlover)
        if current_bait == 'Magnet':
            newQuantity *= 0.9
            if newQuality >= 1.1:
                newQuality -= 0.1
            elif newQuality > 1:
                newQuality = 1
            newTreasure *= (1.75 * baitlover)
        if current_bait == 'Magic':
            newQuantity *= (1.35 * baitlover)
            newQuality += (0.3 * baitlover)
            newTreasure *= (1.3 * baitlover)
        bait -= 1


    # Exotic fish catch chance
    if (randint(1, 100) <= newTreasure) and (quik == 'no'):
        if level >= 12:
            loot()
                

    
    global fishies, salmon, cod, tropicalFish, pufferfish, fieryPufferfish, volcanicFish, turtle, squid, dolphin
    
    minRolls = int(newQuantity*5)
    maxRolls = int(newQuantity*10)
    for i in range(randint(minRolls, maxRolls)):

        fishQuality = 0 + int(newQuality)

        global fishies, salmon, cod, tropicalFish, pufferfish, fieryPufferfish, volcanicFish, turtle, squid, dolphin
        
        upgradeChance = 100 * (newQuality % 1)
        if randint(1, 100) <= upgradeChance:
            fishQuality += 1

        if fishQuality == 1:
            fishies += 1
            newFish += 1
        if fishQuality == 2:
            salmon += 1
            newSalmon += 1
        if fishQuality == 3:
            cod += 1
            newCod += 1
        if fishQuality == 4:
            tropicalFish += 1
            newTropicalFish += 1
        if fishQuality == 5:
            pufferfish += 1
            newPufferfish += 1
        if fishQuality == 6:
            fieryPufferfish += 1
            newFieryPufferfish += 1
        if fishQuality == 7:
            volcanicFish += 1
            newVolcanicFish += 1
        if fishQuality == 8:
            turtle += 1
            newTurtle += 1
        if fishQuality == 9:
            squid += 1
            newSquid += 1
        if fishQuality >= 10:
            dolphin += 1
            newDolphin += 1

    def display_caught_fish():
        global fish_type, xp, newXP, xm
        fish_dict = {
            'Fish': newFish,
            'Salmon': newSalmon,
            'Cod': newCod,
            'Tropical Fish': newTropicalFish,
            'Pufferfish': newPufferfish,
            'Fiery Pufferfish': newFieryPufferfish,
            
            'Volcanic Fish': newVolcanicFish,
            'Turtle': newTurtle,
            'Squid': newSquid,
            'Dolphin': newDolphin
        }

        totalXP = 0
        for fish_type, quantity in fish_dict.items():
            if quantity > 0:
                print(f'You caught {quantity} {fish_type}!')
                if fish_type in fish_xp_values:
                    totalXP += (fish_xp_values[fish_type] * quantity) * xm
                    xp += totalXP 

        # Move the print statement here
        print('+' + str(int(totalXP)) + ' XP')
        if quik == 'no':
            check_level_up()

    # Call the function at the end of your fish() function
    display_caught_fish()


    if baitover == True:
        print('You ran out of ' + current_bait + '.')

    if fishover == True:
        print('Your fish boost ended!')

    if catchover == True:
        print('Your catch boost ended!')

    if treasureover == True:
        print('Your treasure boost ended!')

    if (randint(1, 150) == 1):
        if quik == 'no':
            tip = randint(1, 10)
            if tip == 1:
                print('\nTIP: Make sure to always use bait!')
            if tip == 2:
                print('\nTIP: Exotic fish have a 1 in 100 base chance to be caught.')
            if tip == 3:
                print('\nTIP: Each boost lasts for 200 fishing trips.')
            if tip == 4:
                print('\nTIP: Once you fish with enough money, you will win the game.')
            if tip == 5:
                print('\nTIP: Before selling your fish, check to see if you have enough to purchase a Salesmen upgrade.')
            if tip == 6:
                print('\nTIP: The magnet bait has a highest treasure chance, almost doubling it.')
            if tip == 7:
                print('\nTIP: The bait lover upgrade only affects positive bonuses.')
            if tip == 8:
                print('\nTIP: The maximum fish quality factor obtainable is 9.6, allowing you to catch dolphin.')
            if tip == 9:
                print('\nTIP: The maximum treasure chance is 18.375%.')
            if tip == 10:
                print('\nTIP: Quick Fish instantly fishes for you, but you can\'t catch exotics.')

charm_levels = {
    "Shiny Charm": [0, 0, 1],
    "Economy Charm": [0, 0, 1],
    "Lucky Charm": [0, 0, 1],
    "Storage Charm": [0, 0, 1],
    "Olden Charm": [0, 0, 1]
}



# Define the function to level up the charms
def level_up_charm(charm):
    global xm, quality, quantity, multi, upgrader, exotic

    # Check if the charm can be leveled up
    if (charm_levels[charm][0] >= charm_levels[charm][2]) and charm_levels[charm][1] < 5:
        # Level up the charm
        charm_levels[charm][0] -= charm_levels[charm][2]
        charm_levels[charm][1] += 1
        charm_levels[charm][2] += 1

        if charm_levels[charm][1] == 5:
            charm_levels[charm][2] = 0
        # Update the corresponding variable
        if charm == "Shiny Charm":
            quality += 0.1
        elif charm == "Economy Charm":
            multi *= 1.05
        elif charm == "Lucky Charm":
            upgrader += 1
        elif charm == "Storage Charm":
            quantity *= 1.05
        elif charm == "Olden Charm":
            xm *= 1.1

        print(f"You found a {charm}!")
        print(f"{charm} has been leveled up to level {charm_levels[charm][1]}!")

    elif charm_levels[charm][1] == 5:
        print(f"You found a {charm}!")
        print(f"{charm} is already at max level. You received 5 exotic fish as compensation.")
        # Add 5 exotic fish to the player's inventory
        exotic += 5
    else:
        print(f"You found a {charm}!")

def getCharm():
    charmval = randint(1, 5)
    if charmval == 1: charmval = 'Shiny Charm'
    if charmval == 2: charmval = 'Economy Charm'
    if charmval == 3: charmval = 'Lucky Charm'
    if charmval == 4: charmval = 'Storage Charm'
    if charmval == 5: charmval = 'Olden Charm'
    charm_levels[charmval][0] += 1
    level_up_charm(charmval)

def loot():
    global money, xp, level, exotic
    value = level
    if level >= 20:
        value *= 2
    if level >= 30:
        value *= 2
    if level >= 40:
        value *= 2
    if level >= 50:
        value *= 2
    if level >= 60:
        value *= 2
    if level >= 65:
        value *= 2
    if level >= 70:
        value *= 2
    if level >= 73:
        value *= 2
    if level >= 75:
        value *= 2
    if level >= 80:
        value *= 2

    rv = randint(1, 1000)
    if rv >= (990 - upgrader):
        rarity = 6
    elif rv >= (970 - upgrader*2):
        rarity = 5
    elif rv >= (890 - upgrader*4):
        rarity = 4
    elif rv >= (700-upgrader*8):
        rarity = 3
    elif rv >= (400-upgrader*16):
        rarity = 2
    else:
        rarity = 1

    if level >= 25:
        if level >= 50:
            if rarity == 1:
                print('\nYou found a Common Crate.')
                if randint(1, 100) == 1:
                    getCharm()
                elif randint(1, 3) == 1:
                    value *= randint(75, 150)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(20, 35)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(1, 3)
                    exotic += newExotic
                    print('You got ' + ('an' if newExotic == 1 else str(newExotic)) + ' exotic fish from it.')
            if rarity == 2:
                print('\nYou found an Uncommon Crate.')
                if randint(1, 50) == 1:
                    getCharm()
                elif randint(1, 3) == 1:
                    value *= randint(150, 250)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(35, 50)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(2, 4)
                    exotic += newExotic
                    print('You caught ' + ('an' if newExotic == 1 else str(newExotic))+  ' exotic fish from it.')
            if rarity == 3:
                print('\nSweet! You found a Rare Crate.')
                if randint(1, 30) == 1:
                    getCharm()
                elif randint(1, 3) == 1:
                    value *= randint(250, 500)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(50, 100)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(3, 5)
                    exotic += newExotic
                    print('You caught ' + ('an' if newExotic == 1 else str(newExotic))+  ' exotic fish from it.')
            if rarity == 4:
                print('\nNice! You found a Epic Crate!')
                if randint(1, 15) == 1:
                    getCharm()
                elif randint(1, 3) == 1:
                    value *= randint(500, 800)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(100, 160)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(4, 7)
                    exotic += newExotic
                    print(f'You got {newExotic} exotic fish from it.')
            if rarity == 5:
                print('\nWOW! You found a LEGENDARY Crate!!')
                if randint(1, 8) == 1:
                    getCharm()
                elif randint(1, 3) == 1:
                    value *= randint(800, 1250)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(160, 230)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(6, 9)
                    exotic += newExotic
                    print(f'You caught {newExotic} exotic fish from it.')
            if rarity == 6:
                print('\nYOU FOUND A MYTHIC CRATE!!!')
                if randint(1, 2) == 1:
                    getCharm()
                elif randint(1, 3) == 1:
                    value *= randint(1250, 2000)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(230, 300)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(8, 12)
                    exotic += newExotic
                    print(f'You caught {newExotic} exotic fish from it.')
        else:
            if rarity == 1:
                print('\nYou found a Common Crate.')
                if randint(1, 3) == 1:
                    value *= randint(75, 150)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(20, 35)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(1, 3)
                    exotic += newExotic
                    print('You got ' + ('an' if newExotic == 1 else str(newExotic)) + ' exotic fish from it.')
            if rarity == 2:
                print('\nYou found an Uncommon Crate.')
                if randint(1, 3) == 1:
                    value *= randint(150, 250)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(35, 50)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(2, 4)
                    exotic += newExotic
                    print('You caught ' + ('an' if newExotic == 1 else str(newExotic))+  ' exotic fish from it.')
            if rarity == 3:
                print('\nSweet! You found a Rare Crate.')
                if randint(1, 3) == 1:
                    value *= randint(250, 500)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(50, 100)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(3, 5)
                    exotic += newExotic
                    print('You caught ' + ('an' if newExotic == 1 else str(newExotic))+  ' exotic fish from it.')
            if rarity == 4:
                print('\nNice! You found a Epic Crate!')
                if randint(1, 3) == 1:
                    value *= randint(500, 800)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(100, 160)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(4, 7)
                    exotic += newExotic
                    print(f'You got {newExotic} exotic fish from it.')
            if rarity == 5:
                print('\nWOW! You found a LEGENDARY Crate!!')
                if randint(1, 3) == 1:
                    value *= randint(800, 1250)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(160, 230)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(6, 9)
                    exotic += newExotic
                    print(f'You caught {newExotic} exotic fish from it.')
            if rarity == 6:
                print('\nYOU FOUND A MYTHIC CRATE!!!')
                if randint(1, 3) == 1:
                    value *= randint(1250, 2000)
                    money += value
                    print(f'You got ${value} from it.\n')
                elif randint(1, 2) == 1:
                    value *= randint(230, 300)
                    xp += value
                    print(f'You got {value} XP from it.\n')
                else:
                    newExotic = randint(8, 12)
                    exotic += newExotic
                    print(f'You caught {newExotic} exotic fish from it.')
    else:
        if rarity == 1:
            print('\nYou found a Common Crate.')
            if randint(1, 2) == 1:
                value *= randint(75, 150)
                money += value
                print(f'You got ${value} from it.\n')
            else:
                value *= randint(20, 35)
                xp += value
                print(f'You got {value} XP from it.\n')
        if rarity == 2:
            print('\nYou found an Uncommon Crate.')
            if randint(1, 2) == 1:
                value *= randint(150, 250)
                money += value
                print(f'You got ${value} from it.\n')
            else:
                value *= randint(35, 50)
                xp += value
                print(f'You got {value} XP from it.\n')
        if rarity == 3:
            print('\nSweet! You found a Rare Crate.')
            if randint(1, 2) == 1:
                value *= randint(250, 500)
                money += value
                print(f'You got ${value} from it.\n')
            else:
                value *= randint(50, 100)
                xp += value
                print(f'You got {value} XP from it.\n')
        if rarity == 4:
            print('\nNice! You found a Epic Crate!')
            if randint(1, 2) == 1:
                value *= randint(500, 800)
                money += value
                print(f'You got ${value} from it.\n')
            else:
                value *= randint(100, 160)
                xp += value
                print(f'You got {value} XP from it.\n')
        if rarity == 5:
            print('\nWOW! You found a LEGENDARY Crate!!')
            if randint(1, 2) == 1:
                value *= randint(800, 1250)
                money += value
                print(f'You got ${value} from it.\n')
            else:
                value *= randint(160, 230)
                xp += value
                print(f'You got {value} XP from it.\n')
        if rarity == 6:
            print('\nYOU FOUND A MYTHIC CRATE!!!')
            if randint(1, 2) == 1:
                value *= randint(1250, 2000)
                money += value
                print(f'You got ${value} from it.\n')
            else:
                value *= randint(230, 300)
                xp += value
                print(f'You got {value} XP from it.\n')      
        
            

def inventory():
    print('\n')
    sleep(0.15)
    fish_dict = {
        'Fish': fishies,
        'Salmon': salmon,
        'Cod': cod,
        'Tropical Fish': tropicalFish,
        'Pufferfish': pufferfish,
        'Fiery Pufferfish': fieryPufferfish,
        'Volcanic Fish': volcanicFish,
        'Turtle': turtle,
        'Squid': squid,
        'Dolphin': dolphin,
        'Exotic Fish': exotic
    }

    for fish_type, quantity in fish_dict.items():
        if quantity > 0:
            print(f'You have {quantity} {fish_type}.')
            sleep(0.15)

    print('You have $' + str(int(money)) + '.')
    sleep(0.15)
    if fishboost > 0:
        print('\nYou have ' + str(fishboost) + ' fish boosts.')
        sleep(0.15)
    if catchboost > 0:
        print('You have ' + str(catchboost) + ' catch boosts.')
        sleep(0.15)
    if treasureboost > 0:
        print('You have ' + str(treasureboost) + ' treasure boosts.')
        sleep(0.15)

    if bait > 0:
        print('You have', bait, current_bait + '.')
        sleep(0.15)
        


def sell():
    print('\n')
    global money
    global fishies, salmon, cod, tropicalFish, pufferfish, fieryPufferfish, volcanicFish, turtle, squid, dolphin

    # Conversion rates
    rates = {
        'Fish': 1,
        'Salmon': 3,
        'Cod': 10,
        'Tropical Fish': 30,
        'Pufferfish': 80,
        'Fiery Pufferfish': 200,
        'Volcanic Fish': 480,
        'Turtle': 1000,
        'Squid': 2500,
        'Dolphin': 6000
    }

    # Inventory
    fish_dict = {
        'Fish': fishies,
        'Salmon': salmon,
        'Cod': cod,
        'Tropical Fish': tropicalFish,
        'Pufferfish': pufferfish,
        'Fiery Pufferfish': fieryPufferfish,
        'Volcanic Fish': volcanicFish,
        'Turtle': turtle,
        'Squid': squid,
        'Dolphin': dolphin
    }

    # Sell the fish
    for fish_type, amount in fish_dict.items():
        if amount > 0:
            money += rates[fish_type] * amount * multi
            print(f'Sold {amount} {fish_type} for ${rates[fish_type] * amount}.')
            # Reset the quantity of sold fish to zero
            fish_dict[fish_type] = 0
    
    print('\nYou now have $' + str(int(money)) + '.')
    fishies = 0
    salmon = 0
    cod = 0
    tropicalFish = 0
    pufferfish = 0
    fieryPufferfish = 0
    volcanicFish = 0
    turtle = 0
    squid = 0
    dolphin = 0

# Define the upgrade levels and costs
upgrade_levels = {
    'More Fish': [0, 15]
}

upgrade_costs = {
    'More Fish': [200, 500, 1500, 5000, 12500, 30000, 75000, 200000, 500000, 1500000, 5000000, 15000000, 50000000, 150000000, 500000000]
}

def upgradeShop():
    global money, quantity, quality, multi, boostbooster, baitlover, treasure, xm
    while True:
        print("Upgrade Shop:")
        sleep(0.01)
        print('Your current balance is $' + str(int(money)) + '.\n')
        sleep(0.01)
        for i, upgrade in enumerate(upgrade_levels.keys(), start=1):
            currlevel, max_level = upgrade_levels[upgrade]
            if currlevel < max_level:
                cost = upgrade_costs[upgrade][currlevel]
                print(f"{i}: {upgrade}: Level {currlevel}/{max_level}: ${cost}")
            else:
                print(f"{i}: {upgrade}: MAX LEVEL")
            sleep(0.01)
        print("Enter the number of the upgrade you want to buy, or 'back' to go back.")
        print("Enter 'help' to learn about each upgrade.")
        
        user_input = input("")
        if user_input.lower() == 'back':
            break

        if user_input.lower() == 'help':
            print('More Fish increases the amount of fish you catch.')
            sleep(0.1)
            if level >= 6:
                print('Better Fish increases the quality of fish you catch.')
                sleep(0.1)
            if level >= 8:
                print('Salesmen increases the sell value of your fish.')
                sleep(0.1)
            if level >= 11:
                print('Experienced increases the amount of xp you get.')
            if level >= 35:
                print('Boost Booster increases the effectiveness of boosters.')
                sleep(0.1)
            if level >= 45:
                print('Bait Lover increases the effectiveness of bait.')
                sleep(0.1)
            if level >= 55:
                print('Treasure Hoarder increases the chance for treasure.\n')
                sleep(0.1)
        
        elif user_input.isdigit():
            upgrade_index = int(user_input) - 1
            if upgrade_index >= 0 and upgrade_index < len(upgrade_levels):
                upgrade = list(upgrade_levels.keys())[upgrade_index]
                currlevel, max_level = upgrade_levels[upgrade]
                if currlevel < max_level:
                    cost = upgrade_costs[upgrade][currlevel]
                    if money >= cost:
                        money -= cost
                        upgrade_levels[upgrade][0] += 1
                        print(f"\nBought {upgrade} level {upgrade_levels[upgrade][0]} for ${cost}.\n")
                        if upgrade == 'More Fish':
                            quantity *= 1.12
                        elif upgrade == 'Better Fish':
                            quality = quality + 0.12
                        elif upgrade == 'Salesmen':
                            multi *= 1.2
                        elif upgrade == 'Treasure Hoarder':
                            treasure += 0.1
                        elif upgrade == 'Bait Lover':
                            baitlover += 0.05
                        elif upgrade == 'Boost Booster':
                            boostbooster += 0.05
                        elif upgrade == 'Experienced':
                            xm += 0.2
                    else:
                        print("\nYou don't have enough money.\n")
                else:
                    print("\nThis upgrade is already at max level.\n")
            else:
                print("\nInvalid command. Please enter a valid number.\n")
        else:
            print("\nInvalid command. Please enter a valid number.\n")
        sleep(0.25)

rod_levels = {
    'Dirt Rod': [1, 0],
    'Plastic Rod': [0, 500],
}

# Define the current rod
current_rod = 'Dirt Rod'

def rods():
    global money, current_rod
    while True:
        print("Rod Shop:")
        sleep(0.015)
        print('Rods increase the amount and quality of fish you catch.')
        sleep(0.2)
        print('Your current balance is $' + str(int(money)) + '.\n')
        sleep(0.015)
        for i, rod in enumerate(rod_levels.keys(), start=1):
            level, cost = rod_levels[rod]
            if level == 1:
                if rod == current_rod:
                    print(f"{i}: {rod} (Selected)")
                else:
                    print(f"{i}: {rod} (Owned)")
            else:
                print(f"{i}: {rod} - ${cost}")
            sleep(0.015)
        print("Enter the number of the rod you want to buy or select, or 'back' to go back.")
        
        user_input = input("")
        if user_input.lower() == 'back':
            break

        if user_input.isdigit():
            rod_index = int(user_input) - 1
            if rod_index >= 0 and rod_index < len(rod_levels):
                rod = list(rod_levels.keys())[rod_index]
                level, cost = rod_levels[rod]
                if level == 1:
                    if rod == current_rod:
                        print("\nThis rod is already selected.\n")
                    else:
                        current_rod = rod
                        print(f"\n{rod} is now selected.\n")
                else:
                    if money >= cost:
                        money -= cost
                        rod_levels[rod][0] = 1
                        current_rod = rod
                        print(f"\nBought {rod} for ${cost}.\n")
                    else:
                        print("\nYou don't have enough money.\n")
            else:
                print("\nInvalid command. Please enter a valid number.\n")
        else:
            print("\nInvalid command. Please enter a valid number.\n")
        sleep(0.25)

# Define the boat levels and costs
boat_levels = {
    'Raft': [1, 0],
    'Canoe': [0, 500],
}

# Define the current boat
current_boat = 'Raft'


def boats():
    global money, current_boat
    while True:
        print("Boat Shop:")
        print('Boats slightly increase the quality of fish you catch and increase the chance to get treasure.')
        sleep(0.25)
        print('Your current balance is $' + str(int(money)) + '.\n')
        for i, boat in enumerate(boat_levels.keys(), start=1):
            level, cost = boat_levels[boat]
            if level == 1:
                if boat == current_boat:
                    
                    print(f"{i}: {boat} (Selected)")
                else:
                    print(f"{i}: {boat} (Owned)")
            else:
                print(f"{i}: {boat} - ${cost}")
            sleep(0.015)
        print("Enter the number of the boat you want to buy or select, or 'back' to go back.")
        sleep(0.015)
        user_input = input("")
        if user_input.lower() == 'back':
            break

        if user_input.isdigit():
            boat_index = int(user_input) - 1
            if boat_index >= 0 and boat_index < len(boat_levels):
                boat = list(boat_levels.keys())[boat_index]
                level, cost = boat_levels[boat]
                if level == 1:
                    if boat == current_boat:
                        print("\nThis boat is already selected.\n")
                    else:
                        current_boat = boat
                        print(f"\n{boat} is now selected.\n")
                else:
                    if money >= cost:
                        money -= cost
                        boat_levels[boat][0] = 1
                        current_boat = boat
                        print(f"\nBought {boat} for ${cost}.\n")
                    else:
                        print("\nYou don't have enough money.\n")
            else:
                print("Invalid command. Please enter a valid number.")
        else:
            print("Invalid command. Please enter a valid number.")
        sleep(0.25)
boost_levels = {
    'Fish Boost': [0, 'Increases the amount of fish caught.'],
}

def boost():
    global exotic, fishboost, catchboost, treasureboost, multi, boostbooster
    while True:
        print("Boost Shop:")
        sleep(0.02)
        print("You have " + str(int(exotic)) + " Exotic Fish. Each boost costs 10.")
        sleep(0.015)
        print("Boosts temporarily increase your stats.\n")
        sleep(0.1)
        for i, boost in enumerate(boost_levels.keys(), start=1):
            level, cost = boost_levels[boost]
            print(f"{i}: {boost} - {cost}")
            sleep(0.015)
        print("Enter the number of the boost you want to buy, or 'back' to go back.")
        
        user_input = input("")
        if user_input.lower() == 'back':
            break

        if user_input.isdigit():
            boost_index = int(user_input) - 1
            if boost_index >= 0 and boost_index < len(boost_levels):
                boost = list(boost_levels.keys())[boost_index]
                level, cost = boost_levels[boost]
                if exotic >= 10:
                    exotic -= 10
                    if boost == 'Fish Boost':
                        fishboost += 200
                    elif boost == 'Catch Boost':
                        catchboost += 200
                    elif boost == 'Treasure Boost':
                        treasureboost += 200
                    print(f"\nBought {boost} for {cost} Exotic Fish.")
                    sleep(0.015)
                    if boost != 'Quick Fish':
                        print('This boost will last for the next 200 fishing trips.\n')
                    else:
                        print('Executing Quick Fish...')
                        sleep(0.5)
                        for i in range(100*boostbooster):
                            fish('yes')
                        for i in range(5):
                            check_level_up()
                        print('\n\n')
                else: print("\nYou don't have enough Exotic Fish.\n")
            else: print("\nInvalid command. Please enter a valid number.\n")
        else: print("\nInvalid command. Please enter a valid number.\n")
        sleep(0.25)


# Define a function to check if the player has enough experience to level up
def check_level_up():
    global level, xp, xpnext, multi, treasure, quantity

    # Check if the player's experience is greater than or equal to the experience required for the next level
    if xp >= xpnext and level < 80:
        # Level up the player
        level += 1

        # Subtract the required experience for the level up
        xp -= xpnext

        # Increase the experience required for the next level exponentially
        xpnext *= 1.187467794  # Adjust this value to change the rate of exponential growth

        # Print a message to the player
        print(f"\nLEVEL UP! You are now Level {level}.")

        if level == 2:
            print('You have unlocked sell! Type sell to sell your catch and get money!')

        if level == 3:
            print('You have unlocked inventory! Type inv to see all your types of fish and money!')

        if level == 4:
            print('You have unlocked rods! Type rods to buy or select a rod.')
            print('Rods help increase the amount and quality of fish you get!')
            print('More rods will be added as you level up!')

        if level == 5:
            print('You have unlocked upgrades. Type upgrades to see your upgrades.')
            print('Upgrades are permanent stat boosts that help you fish.')
            print('They can be leveled up multiple times.')
            print('More upgrades will be unlocked as you level up.')

        if level == 6:
            print('You have unlocked the Better Fish upgrade!')
            print('The better fish upgrade increases the quality of fish.')
            print('Find it in the upgrades menu!')
            upgrade_levels['Better Fish'] = [0, 20]
            upgrade_costs['Better Fish'] = [200, 400, 750, 1500, 2500, 5000, 10000, 20000, 45000, 100000, 250000, 600000, 1500000, 3000000, 6000000, 12500000, 25000000, 50000000, 150000000, 500000000]

        if level == 7:
            print('You have unlocked stats! Type stat to see all your stats.')

        if level == 8:
            print('You have unlocked the salesmen upgrade! The salesmen upgrade increases your sell multiplier.')
            print('Sell multiplier increases the value of fish when sold.')
            print('The sell multiplier has been added to your stats menu.')
            upgrade_levels['Salesmen'] = [0, 20]
            upgrade_costs['Salesmen'] = [200, 400, 750, 1500, 2500, 5000, 10000, 20000, 45000, 100000, 250000, 600000, 1500000, 3000000, 6000000, 12500000, 25000000, 50000000, 150000000, 500000000]

        if level == 9:
            print('Another rod has been added to the rod shop.')
            rod_levels['Improved Rod'] = [0, 4000]
        
        if level == 10:
            print('You have unlocked bait! Type bait to see the bait you can buy.')
            print('Bait is consumed on each fishing trip and improves various stats.')

        if level == 11:
            print('You have unlocked the experienced upgrade!')
            print('The experienced upgrade increases the amount of experience you get.')
            upgrade_levels['Experienced'] = [0, 20]
            upgrade_costs['Experienced'] = [200, 400, 750, 1500, 2500, 5000, 10000, 20000, 45000, 100000, 250000, 600000, 1500000, 3000000, 6000000, 12500000, 25000000, 50000000, 150000000, 500000000]

        if level == 12:
            print('You have unlocked treasure!')
            print('Treasure has a small chance to be caught while fishing.')
            print('Type stat to see your treasure chance!')

        if level == 13:
            print('You have unlocked a free 10% sell multiplier.')
            multi *= 1.1

        if level == 14:
            print('You have unlocked a free 10% treasure chance boost.')
            treasure *= 1.1

        if level == 15:
            print('You have unlocked boats! Type boats to see the boats you can buy.')
            print('Boats increase the chance for treasure and the amount of fish caught!')

        if level == 16:
            print('A new boat has been added to the boat shop.')
            boat_levels['Sailboat'] = [0, 4000]

        if level == 17:
            print('You have unlocked a free 2% fish quantity upgrade.')
            quantity *= 1.02
        
        if level == 18:
            print('Another rod has been added to the rod shop.')
            rod_levels['Greater Rod'] = [0, 25000]

        if level == 19:
            print('You have unlocked a free 5% treasure chance boost.')
            treasure *= 1.05

        if level == 20:
            print('You have unlocked a new type of bait, leeches.')
            print('Leeches don\'t get as much fish but the quality is much higher.')
            bait_levels['Leeches'] = [0, 25]

        if level == 21:
            print('You have unlocked a free 5% treasure chance boost.')
            treasure *= 1.05


        if level == 22:
            print('A new boat has been added to the boat shop.')
            boat_levels['Motor Boat'] = [0, 25000]


        if level == 24:
            print('Another rod has been added to the rod shop.')
            rod_levels['Fiberglass Rod'] = [0, 125000]

        if level == 25:
            print('You have unlocked boosts! Type boosts to see all the various boosts.')
            print('Boosts come in many different types and heavily boost stats.')
            print('They don\'t last forever, though!')
            print('More boosts will be added as you level up.')
            print('\nIn order to obtain boosts, you must catch exotic fish.')
            print('Exotic fish is a type of treasure.')

        if level == 26:
            print('A new boat has been added to the boat shop.')
            boat_levels['Speed Boat'] = [0, 125000]

        if level == 27:
            print('You have unlocked a free 5% treasure chance boost.')
            treasure *= 1.05

        if level == 28:
            print('Another rod has been added to the rod shop.')
            rod_levels['Lava Rod'] = [0, 1000000]
            
        if level == 30:
            print('You have unlocked the magnet bait! Buy it in the bait shop.')
            print('The magnet bait increases your treasure chance drastically.')
            bait_levels['Magnet'] = [0, 75]

        if level == 31:
            print('A new boat has been added to the boat shop.')
            boat_levels['Catamaran'] = [0, 1000000]

        if level == 32:
            print('You have unlocked the catch boost. Find it in the boost shop.')
            print('The catch boost increases the quality of fish caught.')
            boost_levels['Catch Boost'] = [0, 'Increases the quality of fish caught.']

        if level == 33:
            print('Another rod has been added to the rod shop.')
            rod_levels['Magma Rod'] = [0, 10000000]
        
        if level == 35:
            print('A new boat has been added to the boat shop.')
            boat_levels['Pontoon'] = [0, 10000000]

        if level == 37:
            print('You have unlocked a free 5% treasure boost!')
            treasure *= 1.05

        if level == 38:
            print('Another rod has been added to the rod shop.')
            rod_levels['Treasure Rod'] = [0, 50000000]

        if level == 40:
            print('You have unlocked Magic Bait! Buy it in the rod shop.')
            print('The magic bait improves the amount and quality of fish caught, ')
            print('as well as the treasure.')
            bait_levels['Magic'] = [0, 250]

        if level == 43:
            print('You have unlocked the treasure boost! Find it in the boost shop.')
            print('The treasure boost increases your treasure chance!')
            boost_levels['Treasure Boost'] = [0, 'Increases the chance for treasure.']


        if level == 45:
            print('You have unlocked the bait lover upgrade.')
            print('The bait lover increases the effectiveness of bait.')
            upgrade_levels['Bait Lover'] = [0, 10]
            upgrade_costs['Bait Lover'] = [500, 2500, 12000, 50000, 250000, 1000000, 5000000, 20000000, 100000000, 500000000]

        if level == 46:
            print('Another rod has been added to the rod shop.')
            rod_levels['Oceanic Rod'] = [0, 75000000]

        if level == 47:
            print('You have unlocked a free 5% treasure boost!')
            treasure *= 1.05

        if level == 48:
            print('A new boat has been added to the boat shop.')
            boat_levels['Ship'] = [0, 75000000]


        if level == 50:
            print('You have unlocked charms! Charms can be obtained from treasure.')
            print('Charms provide various bonuses and are extremely rare.')
            print('Type "charms" to see your charms.')

        if level == 55:
            print('You have unlocked the treasure hoarder upgrade.')
            print('The treasure hoarder upgrade increases the chance of treasure.')
            upgrade_levels['Treasure Hoarder'] = [0, 10]
            upgrade_costs['Treasure Hoarder'] = [500, 2500, 12000, 50000, 250000, 1000000, 5000000, 20000000, 100000000, 500000000]

        if level == 58:
            print('Another rod has been added to the rod shop.')
            rod_levels['Aquatic Rod'] = [0, 500000000]

        if level == 60:
            print('A new boat has been added to the boat shop.')
            boat_levels['Fishing Boat'] = [0, 500000000]

        if level == 65:
            print('You have unlocked the boost booster upgrade.')
            print('The boost booster increases the effectiveness of boosts.')
            upgrade_levels['Boost Booster'] = [0, 10]
            upgrade_costs['Boost Booster'] = [500, 2500, 12000, 50000, 250000, 1000000, 5000000, 20000000, 100000000, 500000000]
            
        if level == 70:
            print('Another rod has been added to the rod shop.')
            rod_levels['Golden Rod'] = [0, 2500000000]

        if level == 72:
            print('A new boat has been added to the boat shop.')
            boat_levels['Cruise'] = [0, 2500000000]

        if level == 75:
            print('You have unlocked the Quick Fish Boost!')
            print('The quick fish immediately fishes for you many times.')
            boost_levels['Quick Fish'] = [0, 'Immediately fishes for you!']
            
        if level == 80:
            print('You have reached the MAX Level.')

# Define the bait levels and costs
bait_levels = {
    'Worms': [0, 4],
}

# Define the current bait
current_bait = 'None'
bait = 0

def baitShop():
    global money, current_bait, bait
    while True:
        print("Bait Shop:")
        sleep(0.015)
        print(f'Your current balance is $' + str(int(money)) + '.')
        sleep(0.015)
        if bait > 0 and current_bait != None:
            print(f'You currently have {bait} {current_bait}.\n')
            sleep(0.15)
        else:
            print('You currently have no bait selected. Buy bait below.')
            sleep(0.15)

        print('Bait improves your stats slightly. Bait is consumed each time you fish. Certain bait types specialize in various things.\n')
        sleep(0.2)
        for i, bait_type in enumerate(bait_levels.keys(), start=1):
            level, cost = bait_levels[bait_type]
            print(f"{i}: {bait_type} - ${cost} each")
            sleep(0.015)
        print("Enter the number of the bait you want to buy, or 'back' to go back.")
        
        user_input = input("")
        if user_input.lower() == 'back':
            break

        if user_input.isdigit():
            bait_index = int(user_input) - 1
            if bait_index >= 0 and bait_index < len(bait_levels):
                bait_type = list(bait_levels.keys())[bait_index]
                cost = bait_levels[bait_type][1]
                while True:
                    amount = (input(f"How much {bait_type} do you want to buy? "))
                    if amount.isdigit() == False:
                        if amount != 'cancel':
                            print('Invalid Number.')
                        if amount == 'cancel':
                            break
                    else: 
                        amount = int(amount)
                        break
                total_cost = cost * amount
                if amount != 'cancel':
                    if money >= total_cost:
                        if bait > 0:
                            confirm = input(f"You already have {bait} {current_bait}. Buying more will discard your current bait. Do you want to continue? (yes/no) ")
                            if confirm.lower() != 'yes':
                                
                                continue
                        money -= total_cost
                        current_bait = bait_type
                        bait = amount
                        
                        print(f"\nBought {bait} {current_bait} for ${total_cost}.\n")
                    else:
                        print("\nYou don't have enough money.\n")
            else:
                print("\nInvalid command. Please enter a valid number.\n")
        else:
            print("\nInvalid command. Please enter a valid number.\n")
        sleep(0.25)

def stats():
    global boostbooster, treasurehoarder, baitlover, level, xm
    newQuality = quality
    newQuantity = quantity
    newTreasure = treasure

    if current_rod == 'Plastic Rod':
        newQuantity *= 1.1
        newQuality += 0.3
    if current_rod == 'Improved Rod':
        newQuantity *= 1.15
        newQuality += 0.6
    if current_rod == 'Greater Rod':
        newQuantity *= 1.25
        newQuality += 1
    if current_rod == 'Fiberglass Rod':
        newQuantity *= 1.35
        newQuality += 1.4
    if current_rod == 'Lava Rod':
        newQuantity *= 1.5
        newQuality += 1.7
    if current_rod == 'Magma Rod':
        newQuantity *= 1.75
        newQuality += 2.0
    if current_rod == 'Oceanic Rod':
        newQuantity *= 2
        newQuality += 2.3
    if current_rod == 'Aquatic Rod':
        newQuantity *= 2.5
        newQuality += 2.6
    if current_rod == 'Golden Rod':
        newQuantity *= 3
        newQuality += 3
    if current_rod == 'Treasure Rod':
        newTreasure *= 2


    # Add boat enhancements
    if current_boat == 'Canoe':
        newQuality += 0.15
        newTreasure *= 1.1
    elif current_boat == 'Sailboat':
        newQuality += 0.3
        newTreasure *= 1.2
    elif current_boat == 'Motor Boat':
        newQuality += 0.45
        newTreasure *= 1.3
    elif current_boat == 'Speed Boat':
        newQuality += 0.6
        newTreasure *= 1.4
    elif current_boat == 'Catamaran':
        newQuality += 0.75
        newTreasure *= 1.5
    elif current_boat == 'Pontoon':
        newQuality += 0.9
        newTreasure *= 1.6
    elif current_boat == 'Ship':
        newQuality += 1.05
        newTreasure *= 1.7
    elif current_boat == 'Fishing Boat':
        newQuality += 1.2
        newTreasure *= 1.8
    elif current_boat == 'Cruise':
        newQuality += 1.5
        newTreasure *= 2.0


    
        
    if fishboost > 0:
        newQuantity *= (1.5 * boostbooster) 
    if catchboost > 0:
        newQuality += (0.5 * boostbooster)
    if treasureboost > 0:
        newTreasure *= (1.5 * boostbooster) 

    if bait > 0:
        if current_bait == 'Worms':
            newQuantity *= (1.4 * baitlover)
        if current_bait == 'Leeches':
            newQuantity *= (1.25 * baitlover)
            newQuality += (0.4 * baitlover)
        if current_bait == 'Magnet':
            newQuantity *= 0.9
            if newQuality >= 1.1:
                newQuality -= 0.1
            elif newQuality > 1:
                newQuality = 1
            newTreasure *= (1.75 * baitlover)
        if current_bait == 'Magic':
            newQuantity *= (1.35 * baitlover)
            newQuality += (0.3 * baitlover)
            newTreasure *= (1.3 * baitlover)
            
    print('Fish Amount Multiplier: ' + str(newQuantity))
    sleep(0.015)
    print('Fish Quality Factor: ' + str(newQuality))
    sleep(0.015)
    
    if level >= 12:
        print('Treasure Chance: ' + str(newTreasure) + '%')
        sleep(0.015)
    if level >= 8:
        print('Sell Multiplier: ' + str(multi))
        sleep(0.015)

def help(level):
    print("List of commands:")
    sleep(0.02)
    print("fish - Start fishing")
    sleep(0.02)
    if level >= 2:
        print("sell - Sell your catch")
        sleep(0.02)
    if level >= 3:
        print("inv or inventory - View your inventory")
        sleep(0.02)
    if level >= 4:
        print("rods - buy or select a fishing rod")
        sleep(0.02)
    if level >= 5:
        print("upgrades - buy upgrades to improve your catch")
        sleep(0.02)
    if level >= 7:
        print('stats - show your current stats')
        sleep(0.02)
    if level >= 10:
        print('bait - buy bait to improve your stats')
        sleep(0.02)
    if level >= 15:
        print("boats - buy or select a boat")
        sleep(0.02)
    if level >= 25:
        print("boosts - temporary boosts that help you fish")
        sleep(0.02)
    print('xp - see your level and progress towards the next')
    sleep(0.02)

def cheat():
    global money
    global xp
    global exotic
    global xpnext, xpc, level
    if xpc == False:
        print('You are lacking permissions to enter the console.')
    else:
        val = input('Enter code: ')
        if val == 'money':
            val = input('Amount: ')
            if val.isdigit() == True:
                money += int(val)
                for i in range(20):
                    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                print('\n$' + val + ' has been added.')
        elif val == 'xp':
            val = input('Amount: ')
            if val.isdigit() == True:
                xp += int(val)
            elif val == 'max':
                xp += 1000000000
            for i in range(20):
                print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
            for i in range(80):
                check_level_up()
        elif val == 'level':
            val = input('Level: ')
            if val.isdigit() == True:
                val = int(val)
                val -= level
                for i in range(20):
                    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                for i in range(int(val)):
                    xp += (xpnext - xp)
                    check_level_up()
                
        elif val == 'exotic':
            if level < 25:
                print('Level 25 required, use "level"')
            else:
                val = input('Amount: ')
                if val.isdigit() == True:
                    exotic += int(val)
                    for i in range(20):
                        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                    print('\n' + val + ' Exotic Fish has been added.')
        elif val == 'chest':
            if level < 12:
                print('Level 12 required, use "level"')
            else:
                val = input('Rolls: ')
                if val.isdigit() == True:
                    for i in range(20):
                        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                    for i in range(int(val)):
                        loot()
        elif val == 'charms':
            if level < 50:
                print('Level 50 required, use "level"')
            else:
                val = input('Rolls: ')
                if val.isdigit() == True:
                    for i in range(20):
                        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
                    for i in range(int(val)):
                        getCharm()

xpc = False
start = True

while True:
    user_input = input("\n")
    if user_input.lower() == "fish":
        fish('no')
        xpc = False
    elif user_input.lower() == "sell":
        if level >= 2:
            sell()
        else: print('You can\'t use this command yet!')
        xpc = False
    elif user_input.lower() in ["inv", "inventory"]:
        if level >= 3:
            inventory()
        else: print('You can\'t use this command yet!')
        xpc = False
    elif user_input.lower() in ['upgrades', 'upgradesshop', 'upgradeshop', 'shop', 'upgrade']:
        if level >= 5: upgradeShop()
        else: print('You can\'t use this command yet!')
        xpc = False
    elif user_input.lower() in ['rod', 'rods', 'rodshop']:
        if level >= 4: rods()
        else: print('You can\'t use this command yet!')
        xpc = False
    elif user_input.lower() in ['boat', 'boats', 'boatshop', 'dock']:
        if level >= 15: boats()
        else: print('You can\'t use this command yet!')
        xpc = False
    elif user_input.lower() in ['boost', 'boosts']:
        if level >= 25: boost()
        else: print('You can\'t use this command yet!')
        xpc = False
    elif user_input.lower() in ['bait', 'baitshop']:
        if level >= 10: baitShop()
        else: print('You can\'t use this command yet!')
        xpc = False
    elif user_input.lower() in ['stat', 'stats', 'viewstats']:
        if level >= 7: stats()
        else: print('You can\'t use this command yet!')
        xpc = False
    elif user_input.lower() == "help":
        help(level)
        xpc = False
    elif user_input.lower() == 'xp':
        print(f'You are level {level}.')
        if level != 80: print(str(int(xp)) + '/' + str(int(xpnext)) + ' XP to level ' + str(level + 1) + '.')
        else: print('This is the max level.')
        xpc = False
    elif user_input.lower() == 'console':
        cheat()
    elif user_input.lower() == 'lock':
        print('The console has been locked.')
        xpc = False
    elif user_input.lower() in ['charm', 'charms']:
        xpc = False
        if level >= 50:
            for charm in charm_levels:
                if charm_levels[charm][1] < 5:
                    print(f"{charm} - Level {charm_levels[charm][1]}: {charm_levels[charm][0]}/{charm_levels[charm][2]}")
                else:
                    print(f"{charm} - MAX LEVEL")

                print('\nThe Shiny Charm makes your rod shinier, allowing you to attract higher quality fish.')
                print('The Economy Charm inflates the economy of fish, allowing you to sell them for more.')
                print('The Lucky Charm makes you luckier, allowing you to get higher rarities of treasure more often.')
                print('The Storage Charm increases the storage of your boat, allowing you to catch more fish during each trip.')
                print('The Olden Charm makes you wiser, allownig you to get more experience.')
        else: print('You can\'t use this command yet!')
    elif user_input.lower() == 'fh':
        xpc = True
        for i in range(3):
            print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

    else:
        print("Invalid command. Please enter 'help' for help.")

    if start == True and user_input.lower() == 'fish':
        print("Welcome to Virtual Fisher, python edition.")
        print("Fish to gain experience. Once you get enough experience you will level up.")
        print("Leveling up unlocks new features.")
        print("Continue to fish to start playing!")
        start = False

    if money >= 50000000000:
        charmsmax = True
        for charm in charm_levels:
            if charm_levels[charm][1] == 5:
                continue
            else:
                charmsmax = False
        if charmsmax == True:
            if level == 80:
                break

print('\n\n\n\n\nCongratulations, you beat the game.')
print('Thank you for playing.')

j = input("")
