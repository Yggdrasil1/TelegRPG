import numpy as np
import json
import copy
import global_variables as gv


class Useable:

    def __init__(self,
                 chatid: int = None,
                 name: str = None,
                 useable_type: str = None,
                 number: int = None,
                 args=None):

        self.chatid = chatid
        self.name = name
        self.useable_type = useable_type
        self.number = number
        self.displayed_name = str(f"{self.name} x {self.number} - {useable_type}")

        if args is not None:
            for a, b in args.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [Useable(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, Useable(b) if isinstance(b, dict) else b)

    def update_displayed_name(self):

        self.displayed_name = f"{self.name} x {self.number} - {self.useable_type}"


class HealConsumable(Useable):

    def __init__(self,
                 chatid: int = None,
                 name: str = None,
                 useable_type: str = None,
                 number: int = None,
                 args=None):
        super().__init__(chatid, name, useable_type, number, args)

    def use(self, inv_place):

        print("used item", self.chatid)

        character = gv.character_dict[self.chatid]

        character.hp += gv.consumable_dict[self.name] * character.max_hp
        if character.hp > character.max_hp:
            character.hp = character.max_hp

        character.hp = int(character.hp)

        return

