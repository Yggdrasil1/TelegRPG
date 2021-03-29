import random
import numpy as np
import global_variables as gv
import math


class Monster:

    def __init__(self, name, difficulty, region_lvl, lvl):

        self.name = name

        self.lvl = lvl

        self.hp = 23 + ((5 + difficulty) * region_lvl)

        self.exp = (2 * region_lvl * (2 + difficulty)).item() + 1

        self.max_hp = self.hp

        self.strength = region_lvl * 4 + self.lvl
        self.dexterity = region_lvl * 4 + self.lvl
        self.intelligence = region_lvl * 4 + self.lvl

        self.dmg = 4 + region_lvl * (5 + difficulty)
        self.armor = 4 + (region_lvl - 1) * (8 + difficulty)

    def __repr__(self):

        return f'lvl: {self.lvl}, max_hp: {self.max_hp}, exp: {self.exp}, \n' \
               f'str: {self.strength}, dex: {self.dexterity}, int: {self.intelligence}'

def competition_function(delta: float, beta=3.0):
    """
    sigmoid competition function
    :param delta:
    :param beta:
    :return:
    """

    return 1. / (1 + np.exp(-beta * delta)) - 0.5


def fight(character1, character2):

    #debug = True

    # determine which character starts the fight || higher dexterity -> hits first
    if character1.dexterity < character2.dexterity:
        char1 = character2
        char2 = character1

    else:
        char1 = character1
        char2 = character2

    # depending on the dexterity difference, calculate dodge chance for char1, char2 can never dodge
    delta_char1 = (char1.dexterity - char2.dexterity) / (2 * char1.dexterity)
    dodge_chance = competition_function(np.abs(delta_char1), gv.dodge_beta_value)

    # calculate crit chances for both chars, higher (+) int diff -> higher crit chance, at least 15%
    int_diff = char1.intelligence - char2.intelligence
    critchance_char1 = (np.power(int_diff, 1.61) / 120 + 15) / 100 if int_diff > 0 else 0.15
    critchance_char2 = (np.power(-int_diff, 1.61) / 120 + 15) / 100 if int_diff < 0 else 0.15

    while char1.hp > 0 and char2.hp > 0:

        char2.hp -= calculate_dmg(char1, char2, critchance_char1)

        if random.random() < dodge_chance:
            pass
        else:
            char1.hp -= calculate_dmg(char2, char1, critchance_char2)

    if character1.hp > 0:

        return character1

    else:
        return character2


def calculate_dmg(char1, armor, crit_chance):
    """
    Function to calculate the dmg char1 deals to char2
    :param char1: Character that deals dmg
    :param armor: Armor of the character that receives the dmg
    :param crit_chance: chance that dmg is doubled
    :return: dmg that is dealt
    """
    if not type(char1) == Monster:
        dmg = char1.calculate_paper_dmg()
    else:
        dmg = char1.dmg

    dmg *= math.sqrt(char1.strength)

    if random.random() < crit_chance:
        dmg *= 2

    return dmg * calculate_dmg_reduction(armor)


def calculate_dmg_reduction(armor):

    if armor > 3.2:
        return 0.07/(np.log10(armor-2))

    else:
        return 1


def spawn_monster(region_lvl, lvl):
    """
    Function to spawn a monster for player "chatID" dependent on the player's position

    :param region_lvl: lvl of the spawned monster
    :return: Monster, monster
    """

    difficulty = np.random.choice(2, 1, p=[0.65, 0.35])[0]

    name = random.choice(list(gv.monster_name_dict[str(region_lvl)].keys()))

    monster_name = random.choice(gv.monster_name_dict[str(region_lvl)][name][str(difficulty + 1)]) + " " + name

    monster = Monster(name=monster_name, difficulty=difficulty, region_lvl=region_lvl, lvl=lvl)

    return monster


def monster_fight(character1, monster):

    debug = True

    # depending on the dexterity difference, calculate dodge chance for character1, monster can never dodge
    delta_char1 = (character1.dexterity - monster.dexterity) / (2 * character1.dexterity)
    if delta_char1 > 0:
        dodge_chance = competition_function(np.abs(delta_char1), gv.dodge_beta_value)
    else:
        dodge_chance = 0

    if debug: print(f'Dodge%: {dodge_chance}')

    # calculate crit chances for both chars, higher (+) int diff -> higher crit chance, at least 15%
    int_diff = character1.intelligence - monster.intelligence
    critchance_char1 = (np.power(int_diff, 1.61) / 120 + 15) / 100 if int_diff > 0 else 0.15
    critchance_char2 = (np.power(-int_diff, 1.61) / 120 + 15) / 100 if int_diff < 0 else 0.15

    if debug: print(f'Monster crit%: {critchance_char2}')
    if debug: print(f'Char crit%: {critchance_char1}')

    monster_armor = monster.armor
    character1.update_armor()
    character1_armor = character1.armor

    # determine which character starts the fight || higher dexterity -> hits first
    if monster.dexterity > character1.dexterity:
        character1.hp -= calculate_dmg(monster, character1_armor, critchance_char2)

    while character1.hp > 0 and monster.hp > 0:

        monster.hp -= calculate_dmg(character1, monster_armor, critchance_char1)

        if debug: print(f"m: {monster.hp}/ {monster.max_hp}")

        if random.random() < dodge_chance:
            pass
        else:
            character1.hp -= calculate_dmg(monster, character1_armor, critchance_char2)

        if debug: print(f"c: {character1.hp}/ {character1.max_hp}")

    if character1.hp > 0:

        return character1

    else:
        return monster


def monster_encounter(character):
    pass