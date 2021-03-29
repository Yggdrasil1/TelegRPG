import numpy as np
import json
import copy
import global_variables as gv
import Useable
import math
import random
import Messages
from Keyboards import *

# -------------------------- A, D,Str,Dex,Int
gear_stat_dict = {"Helmet": [2, 3, 1, 1, 3],
                  "Chest": [0, 5, 3, 2, 1],
                  "Pants": [1, 4, 2, 2, 2],
                  "Boots": [3, 2, 1, 2, 1],
                  "Weapon": [8, 1, 1, 1, 1]}

rarity_bonus = {'common': 1.2,
                'rare': 2,
                'epic': 3}


class Gear:

    def __init__(self,
                 level: int = None,
                 geartype: str = "blubb",
                 rarity: str = "Common",
                 chatID: int = None,
                 name='otto',
                 args=None, ):

        self.lvl = level

        self.chatID = chatID

        self.geartype = geartype

        self.rarity = rarity

        if args is None:

            self.attack = self.initiate_stats(0)

            self.defense = self.initiate_stats(1)

            self.strength = self.initiate_stats(2)

            self.dexterity = self.initiate_stats(3)

            self.intelligence = self.initiate_stats(4)

            self.name = generate_name(geartype, rarity)

        if args is not None:
            for a, b in args.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [Gear(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, Gear(b) if isinstance(b, dict) else b)

    def __repr__(self):
        return f"Stats: {self.attack}, {self.defense}, {self.strength}, " \
               f"{self.dexterity}, {self.intelligence}" # Name: {self.name} , User: {self.chatID},

    def set_stats(self, stats):

        self.attack = stats[0]
        self.defense = stats[1]
        self.strength = stats[2]
        self.dexterity = stats[3]
        self.intelligence = stats[4]
        self.name = stats[5]

    def compare_gear(self, other_gear):

        if not self.geartype == other_gear.geartype:
            pass
        else:
            return self.stats - other_gear.stats

    def initiate_stats(self, stat):

        return int(math.pow(gear_stat_dict[self.geartype][stat] * random.randint(2, 5), 1/2)
                   * rarity_bonus[self.rarity]
                   + math.pow(self.lvl, 1))

    def stats(self):
        return np.array([
            self.attack,
            self.defense,
            self.strength,
            self.dexterity,
            self.intelligence
        ])

    def update_displayed_name(self):
        pass

    def use(self, inv_place):
        inventory = gv.inventory_dict[self.chatID].inv

        print(self.geartype)
        print(inventory['Helmet'])

        helper = inventory[self.geartype]

        inventory[self.geartype] = self

        inventory[inv_place] = helper


def generate_name(geartype, rarity):

    adjective = random.choice(gv.item_name_dict[geartype][rarity]["Addjective"])
    objective = random.choice(gv.item_name_dict[geartype][rarity]["Objective"])
    substantive = random.choice(gv.item_name_dict[geartype][rarity]["Substantive"])

    return f"{adjective} {substantive} {objective}"


class Inventory:

    def __init__(self, chatID, start_inv):

        self.chatID = chatID
        self.inv = {'Helmet': start_inv[0],
                    'Chest': start_inv[1],
                    'Pants': start_inv[2],
                    'Boots': start_inv[3],
                    'Weapon': start_inv[4],
                    'not_equipped01': start_inv[5],
                    'not_equipped02': start_inv[6],
                    'not_equipped03': start_inv[7],
                    'not_equipped04': start_inv[8],
                    'not_equipped05': start_inv[9],
                    'not_equipped06': start_inv[10],
                    'not_equipped07': start_inv[11],
                    'not_equipped08': start_inv[12],
                    'not_equipped09': start_inv[13],
                    'not_equipped10': start_inv[14]}

    def store_inventory(self):
        inv_dict = self.__dict__

        for slot, item in inv_dict['inv'].items():
            if type(item) in [Gear, Useable.HealConsumable, Useable.Useable]:
                inv_dict['inv'][slot] = item.__dict__

        with open(f'D:\\Programme\\telegram_bot\\Character_data\\Inventory\\{inv_dict["chatID"]}', 'w') as f:
            json.dump(inv_dict, f, ensure_ascii=False, indent=4)

    def calculate_paper_dmg(self):
        dmg = [self.inv[x].attack for x in self.inv.keys() if not 'not' in x]
        dmg = np.sum(np.array(dmg))

        return dmg

    def get_total_stat(self, stat: str):

        total_stat = 0
        for item in self.inv:
            if "not_eq" not in item:
                total_stat += getattr(self.inv[item], stat)

        return total_stat

    def calculate_armor(self):
        arm = [self.inv[x].defense for x in self.inv.keys() if not 'not' in x]

        arm = np.sum(np.array(arm))
        if gv.character_debug:
            print(f"calc_armor: {arm}")
        return arm

    def show_not_equipped(self):

        keys = [key for key in self.inv if "not_eq" in key]
        keys.sort()

        return_string = ""

        for key in keys:
            return_string += f"{key[-2:]}: {self.inv[key]} \n"

        return return_string

    def add_item(self, item):

        chatid = self.chatID

        keys = [key for key in self.inv if "not_eq" in key]
        keys.sort()

        full_inventory = True

        for key in keys:
            if self.inv[key] == '-':
                full_inventory = False
                self.inv[key] = item

                gv.bot.send_message(chatid, text=Messages.item_added_to_inv_msg(str(key[-2:]), item.name))

                break

        if full_inventory:
            gv.bot.send_message(chatid,
                                text="Dein Inventar ist leider voll. \n"
                                     "Willst du ein Item zerstören um Platz zu machen?",
                                reply_markup=delete_item_keyboard(self.inv))

            if gv.destroy_item_dict[chatid]:

                keys = [key for key in self.inv if "not_eq" in key]
                keys.sort()

                for key in keys:
                    if self.inv[key] == '-':
                        self.inv[key] = item

    def item_in_inventory(self, item_name):
        keys = [key for key in self.inv if "not_eq" in key]

        item_in_inv = False

        for key in keys:
            if not type(self.inv[key]) == str:
                if self.inv[key].name == item_name:
                    item_in_inv = True

        return item_in_inv


def initial_gear(chatID):

    helmet = Gear(1, 'Helmet', 'common', chatID)  # 2, 3, 1, 1, 3, 'Cap of Startness'
    helmet.set_stats([2, 3, 1, 1, 3, 'Cap of Startness'])

    chest = Gear(1, 'Chest', 'common', chatID)
    chest.set_stats([0, 5, 3, 2, 1, 'Harnish of Startness'])

    pants = Gear(1, 'Pants', 'common', chatID)
    pants.set_stats([1, 4, 2, 2, 2, 'Jeans of Startness'])

    boots = Gear(1, 'Boots', 'common', chatID)
    boots.set_stats([3, 2, 1, 2, 1, 'Shoes of Startness'])

    weapon = Gear(1, 'Weapon', 'common', chatID)
    weapon.set_stats([8, 1, 1, 1, 1,  'Sword of Startness'])

    return [helmet, chest, pants, boots, weapon, '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']


def store_item(slot, item, chatID):
    if not type(item) == str:
        with open(f'D:\\Programme\\telegram_bot\\Character_data\\Inventory\\{chatID}_{slot}', 'w') as f:
            json.dump(item.__dict__, f, ensure_ascii=False, indent=4)
    else:
        with open(f'D:\\Programme\\telegram_bot\\Character_data\\Inventory\\{chatID}_{slot}', 'w') as f:
            json.dump("-", f, ensure_ascii=False, indent=4)


def format_item_text(item):
    if type(item) == Gear:
        return f'{item.attack:<5} {item.defense:<5} {item.strength:<5} {item.dexterity:<5} ' + \
                    f'{item.intelligence:<5}' + f'{item.name} \n'


def initiate_gear_names():

    name_dict = {'Addjective': [],
                 'Substantive': [],
                 'Objective': []
                 }

    rarity_dict = {'common': copy.deepcopy(name_dict),
                   'rare': copy.deepcopy(name_dict),
                   'epic': copy.deepcopy(name_dict)
                   }

    item_name_dict = {'Helmet': copy.deepcopy(rarity_dict),
                      'Pants': copy.deepcopy(rarity_dict),
                      'Chest': copy.deepcopy(rarity_dict),
                      'Boots': copy.deepcopy(rarity_dict),
                      'Weapon': copy.deepcopy(rarity_dict)
                      }

    for item_type in item_name_dict.keys():

        with open(gv.item_names_path + item_type, 'r') as f:
            lines = f.readlines()
            lines = [line.split('\t') for line in lines]

        for line in lines:

            item_name_dict[item_type][line[0].lower()]['Addjective'].append(line[1])

            item_name_dict[item_type][line[0].lower()]['Substantive'].append(
                line[2].replace('-', ' ').replace("\n", ''))
            item_name_dict[item_type][line[0].lower()]['Objective'].append(line[3].replace('-', ' ').replace("\n", ''))

    return item_name_dict

