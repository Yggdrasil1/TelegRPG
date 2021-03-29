import Character
import global_variables as gv
from Messages import *
from Keyboards import *
import Gear
import Create_Images as ci
import numpy as np
import random
import Monster_Spawn
import Useable
import telegram
import time

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def start_new_game(update, context):
    """
    Function to create a new character, add it to the dict of characters and
    lead the game to the class selection
    :param update: standard button argument
    :param context: standard button argument
    """

    query = update.callback_query
    chatid = chatID(query)

    # gv.player_dict.update({chatid: str(chatid)})

    character = Character.Character(chatid)
    gv.character_dict.update({chatid: character})

    inventory = Gear.Inventory(chatid, Gear.initial_gear(chatid))
    gv.inventory_dict.update({chatid: inventory})

    query.answer()
    query.edit_message_text(class_selection_msg(),
                            reply_markup=class_selection_keyboard())


def class_selection(update, context):

    query = update.callback_query
    chatid = chatID(query)

    character = gv.character_dict[chatid]

    character.klasse = query.data
    character.main_stat_increase(5)

    query.edit_message_text(name_selection_msg(),
                            reply_markup=name_selection_keyboard())


def chatID(query):
    return str(query.message.chat.id)


def evaluate_movement(character, direction):

    new_coord_x, new_coord_y = list(np.array(gv.direction_dict[direction]) +
                                    np.array([character.coord_x, character.coord_y]))

    old_region = gv.world_map[character.coord_x][character.coord_y]
    new_region = gv.world_map[new_coord_x][new_coord_y]

    if new_coord_x in [-1, gv.world_max_x + 1] or new_coord_y in [-1, gv.world_max_y - 1]:

        return world_border_reached_msg(), False, "boring"

    elif gv.world_map[new_coord_x][new_coord_y] == 'water':

        return water_reached_msg(), False, "boring"

    else:
        return movement_msg(direction, new_region, old_region, new_coord_x, new_coord_y), True, new_region


def print_inventory(update, context):
    query = update.callback_query
    chatid = chatID(query)

    inventory = gv.inventory_dict[chatid].inv

    string = inventory_msg(inventory)

    query.edit_message_text(text=string)
    gv.bot.send_message(query.message.chat.id, text="Was willst du als nächstes tun?",
                        reply_markup=inventory_keyboard())


def show_useables(update, context):
    query = update.callback_query
    chatid = chatID(query)

    inventory = gv.inventory_dict[chatid]
    query.edit_message_text(text="Das sind die Items die du nicht trägst oder benutzen kannst.")
    gv.bot.send_message(query.message.chat.id, text="Klick auf ein Item um es zu benutzen oder anzulegen.",
                        reply_markup=useable_inventory(inventory))


def delete_item(update, context):

    query = update.callback_query
    chatid = chatID(query)

    inventory = gv.inventory_dict[chatid]

    if not query.data == 'pass':

        item_name = "not_equipped" + query.data[1:]

        inventory[item_name] = '-'

        gv.destroy_item_dict[chatid] = True

    else:
        gv.destroy_item_dict[chatid] = False

    return


def store_data():
    for character in gv.character_dict:
        gv.character_dict[character].store_character()

    for inventory in gv.inventory_dict:
        gv.inventory_dict[inventory].store_inventory()


def send_item(chatid, item):

    image_path = ci.create_item_image(f"{item.geartype.capitalize()}_{item.rarity}", item.stats(), chatid)

    ci.send_image(gv.bot, chatid, image_path, False)

    return


def monster_encounter(character, chatid):

    pre_lvl = character.lvl

    x = character.coord_x
    y = character.coord_y

    region_lvl = gv.monster_lvl_dict[x][y]

    monster = Monster_Spawn.spawn_monster(region_lvl, character.lvl)

    print(monster)

    gv.bot.send_message(chatid, text=monster_spawn_msg(monster.name))

    winner = Monster_Spawn.monster_fight(character, monster)

    if winner == character:

        character.hp = round(character.hp)

        character.exp += monster.exp

        character.update_exp()

        gv.bot.send_message(chatid, text=f"Du hast {character.hp} leben übrig")

        if character.lvl > pre_lvl:

            gv.bot.send_message(chatid, text=lvl_up_msg(character))

        item_drop = random.random()

        gear_type = random.choice(["Helmet", "Chest", "Pants", "Boots", "Weapon"])

        item = "bla"

        if 0.7 < item_drop < 0.85:
            item = Gear.Gear(character.lvl, gear_type, 'common', chatid)

        elif 0.85 < item_drop < 0.95:
            item = Gear.Gear(character.lvl, gear_type, 'rare', chatid)

        elif 0.95 < item_drop:
            item = Gear.Gear(character.lvl, gear_type, 'epic', chatid)

        if not item == 'bla':
            gv.bot.send_message(chatid, text=f"Du hast ein Item gefunden!")
            send_item(chatid, item)
            gv.inventory_dict[chatid].add_item(item)

    else:
        character.hp = 0

        kill_player(character, chatid)

    return


def kill_player(character, chatid):

    character.update_max_hp()

    character.hp = character.max_hp

    character.coord_x = 50
    character.coord_y = 67

    gv.bot.send_message(chatid, text=you_died_msg())

    bread = Useable.HealConsumable(chatid, "Brot", "heilt Leben (30%)", 3)

    if not gv.inventory_dict[chatid].item_in_inventory('Brot'):

        gv.inventory_dict[chatid].add_item(bread)

    return


















