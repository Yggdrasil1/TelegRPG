import Gear
import Character
import global_variables as gv
from Keyboards import *
from Messages import *


def chatID(query):
    return str(query.message.chat.id)


def general_info(update, context):
    query = update.callback_query
    chatid = chatID(query)

    query.edit_message_text(info_main_msg())

    gv.bot.send_message(chatid, text="Was willst du als nächstes tun?",
                        reply_markup=main_menu_keyboard())


def character_info(update, context):
    query = update.callback_query
    chatid = chatID(query)
    print("worked", chatid)
    character = gv.character_dict[chatid]

    query.edit_message_text(character_info_msg(character))

    gv.bot.send_message(chatid, text="Was willst du als nächstes tun?",
                        reply_markup=main_menu_keyboard())