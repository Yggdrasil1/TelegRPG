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
from Bot_Functions import *


def relax_decorator(func):
    def wrapper(*args, **kwargs):
        for a in args:
            if type(a) == telegram.update.Update:
                query = a.callback_query
                chatid = chatID(query)
                character = gv.character_dict[chatid]
                rest_time = int(character.resting_time - int(time.time()))

                if rest_time > 0:
                    query.answer()
                    query.edit_message_text(text="{} Du ruhst dich noch {} sec aus!!".format(u'\U0001F6A8', rest_time),
                                            reply_markup=main_menu_keyboard())
                else:
                    func(*args, **kwargs)

    return wrapper


def send_map(update, context):

    query = update.callback_query

    chatid = chatID(query)

    character = gv.character_dict[chatid]

    image_path = ci.create_map_image(character.coord_x, character.coord_y, chatid)

    ci.send_image(gv.bot, chatid, image_path, False)

    query.answer()

    gv.bot.send_message(query.message.chat.id, text=map_msg(gv.world_map[character.coord_x][character.coord_y]))

    gv.bot.send_message(chatid, text="Was willst du als nächstes tun?",
                        reply_markup=main_menu_keyboard())


@relax_decorator
def move_the_character(update, context):

    query = update.callback_query

    chatid = chatID(query)

    character = gv.character_dict[chatid]

    direction = query.data

    movement_text, movement, new_region = evaluate_movement(character, direction)

    if new_region != "boring":
        pass

    if movement:
        character.char_move(query.data)

    if random.random() > 0.7:
        monster_encounter(character, chatid)

    query.edit_message_text(text=movement_text)

    gv.bot.send_message(query.message.chat.id, text="Was willst du als nächstes tun?",
                        reply_markup=main_menu_keyboard())


@relax_decorator
def use_item(update, context):

    query = update.callback_query
    chatid = chatID(query)

    inventory = gv.inventory_dict[chatid]

    item_name = "not_equipped"+query.data
    item = inventory.inv[item_name]

    if not type(item) == str:

        item.use(item_name)

        if type(item) in [Useable.HealConsumable, Useable.Useable]:
            item.number -= 1

            if item.number == 0:
                inventory.inv[item_name] = "-"

            item.update_displayed_name()

        show_useables(update, context)

    return


@relax_decorator
def relax_character(update, context):
    query = update.callback_query

    chatid = chatID(query)

    character = gv.character_dict[chatid]

    character.resting_time = int(time.time()) + (60*5)

    character.hp = character.max_hp

    rest_time = character.resting_time - int(time.time())

    gv.bot.send_message(query.message.chat.id, text=f"Du ruhst dich jetzt {rest_time}sec lang aus und wirst "
                                                    f"dadurch voll geheilt.",
                        reply_markup=main_menu_keyboard())