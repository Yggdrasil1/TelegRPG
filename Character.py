import json
import numpy as np
from collections import namedtuple
import global_variables as gv
import math


# ----------------------------- Character  ----------------------------- #


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())


def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


class_dict = {'hunter': "Jäger",
              'warrior': "Krieger",
              'mage': 'Magier'}


# ----------------------------- Character  ----------------------------- #


class Character:

    def __init__(self, args):

        if type(args) in [str, int]:
            self.chatID = int(args)

            self.name = ''

            self.klasse = ''

            # --- misc stats --- #

            self.lvl = 1
            self.exp = 0

            self.skill_points = 0

            self.gold = 0

            self.coord_x = 45
            self.coord_y = 71

            self.resting_time = 0

            # --- combat stats --- #
            self.strength = 5
            self.dexterity = 5
            self.intelligence = 5

            self.armor = 4

            # self.luck = 0

            self.max_hp = 30
            self.hp = self.max_hp

        else:
            for a, b in args.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [Character(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, Character(b) if isinstance(b, dict) else b)

    def __repr__(self):
        return str({'name': self.name, 'class': self.klasse, 'lvl': self.lvl,
                    'str, dx, int': [self.strength, self.dexterity, self.intelligence]})

    def char_move(self, direction):

        if (direction == 'up' and self.coord_y == 0) or \
                (direction == 'down' and self.coord_y == gv.world_max_y) or \
                (direction == 'left' and self.coord_x == 0) or \
                (direction == 'right' and self.coord_x == gv.world_max_x):

            return False

        else:
            self.coord_x, self.coord_y = list(np.array(gv.direction_dict[direction]) +
                                              np.array([self.coord_x, self.coord_y]))

            self.coord_x = int(self.coord_x)
            self.coord_y = int(self.coord_y)

            if gv.character_debug: print(f'{self.chatID} moved to {[self.coord_x, self.coord_y]}')

            return True

    def store_character(self):

        self.debug()

        with open(f'D:\\Programme\\telegram_bot\\Character_data\\Character\\{self.chatID}', 'w') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)

        if gv.character_debug:
            print(f"pap_dmg: {self.calculate_paper_dmg()}, pap_arm: {self.armor}")

    def main_stat_increase(self, value_increase):

        stat_increase = gv.main_stat_dict[self.klasse]
        setattr(self, stat_increase, getattr(self, stat_increase) + value_increase)

    def calculate_paper_dmg(self):

        inv = gv.inventory_dict[str(self.chatID)]

        dmg = inv.calculate_paper_dmg()

        main_stat_total = getattr(self, gv.main_stat_dict[self.klasse]) + inv.get_total_stat(
            gv.main_stat_dict[self.klasse])

        dmg *= np.round(math.pow(main_stat_total, 2/3))

        return dmg

    def update_armor(self):
        value = gv.inventory_dict[str(self.chatID)].calculate_armor()
        self.armor = getattr(value, "tolist", lambda: value)()

    def update_max_hp(self):
        self.max_hp = 30 + 2 * self.lvl + \
                      int(math.sqrt(self.strength +
                          gv.inventory_dict[str(self.chatID)].get_total_stat(gv.main_stat_dict[self.klasse])))

    def debug(self):
        for key in self.__dict__.keys():
            print(f"{key}: type: {type(self.__dict__[key])}, value: {self.__dict__[key]}")

    def update_exp(self):

        while self.exp >= int(gv.lvl_dict[str(self.lvl)]):
            self.exp -= int(gv.lvl_dict[str(self.lvl)])
            self.lvl += 1
            self.lvl_up()

    def lvl_up(self):

        print(f"lvl up: {self.name}")

        self.strength += 1
        self.dexterity += 1
        self.intelligence += 1

        self.main_stat_increase(1)

        self.update_max_hp()

    def character_description(self):

        self.update_max_hp()

        inv = gv.inventory_dict[str(self.chatID)]

        return_string = f"Name: {self.name} ({class_dict[self.klasse]}) \n\n" \
                        f"HP: {self.hp}/{self.max_hp} \n" \
                        f"LVL: {self.lvl} ({self.exp}/ {gv.lvl_dict[str(self.lvl)]}) \n\n" \
                        f"---\n\n" \
                        f"Stärke: {self.strength + inv.get_total_stat('strength')} \n" \
                        f"Geschicklichkeit: {self.dexterity + inv.get_total_stat('dexterity')} \n" \
                        f"Intelligenz: {self.intelligence + inv.get_total_stat('intelligence')} \n\n" \
                        f"Damage: {self.calculate_paper_dmg()}"

        return return_string
