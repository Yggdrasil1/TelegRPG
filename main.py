from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler
import Create_Images
from os import listdir
from os.path import isfile, join
import logging
from Character import *
from Bot_Functions import *
from Conv_Handler import conv_handler
import os
import signal
import global_variables as gv
from Keyboards import *
from Messages import *
from Gear import *
from Map import *
from Useable import *
from Info_Texts import *
from Update_Functions import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# ----------------------------- Initiation ----------------------------- #


def initiation():

    # --- Character initialization --- #
    character_path = gv.character_path

    character_files = [f for f in listdir(character_path) if isfile(join(character_path, f))]

    for file_ in character_files:

        with open(character_path+file_) as char_file:
            char_obj = Character.Character(json.load(char_file))

        gv.character_dict[file_] = char_obj

    # --- Inventory initialization --- #

    inventory_path = gv.inventory_path

    inventory_files = [inv_file for inv_file in listdir(inventory_path) if isfile(join(inventory_path, inv_file))]
    for inv_file_ in inventory_files:
        with open(f'{inventory_path}{inv_file_}', 'r') as f:
            e = json.load(f)
        gear_list_dict = [item for slot, item in e['inv'].items()]
        gear_list = []
        for gear in gear_list_dict:
            if gear == '-':
                gear_list.append(gear)
            elif "geartype" in gear.keys():
                gear_list.append(Gear.Gear(args=gear))
            elif "useable_type" in gear.keys():
                if "heilt Leben" == gear['useable_type']:
                    gear_list.append(HealConsumable(args=gear))

        if len(gear_list)<15:
            gear_list.append('-')

        gv.inventory_dict[str(inv_file_)] = Inventory(inv_file_, gear_list)

    gv.item_name_dict = initiate_gear_names()

    # --- Monster Name initialization --- #

    with open("D:\\Programme\\telegram_bot\\Mob_names\\monster_name_dict", "r") as f:
        gv.monster_name_dict = json.load(f)

    # --- World initialization --- #

    initiate_world()

    print("Initiation complete")

    # --- lvl_dict --- #

    with open("D:\\Programme\\telegram_bot\\lvl_exp", "r") as f:
        gv.lvl_dict = json.load(f)

    # --- consumable_dict --- #

    with open("D:\\Programme\\telegram_bot\\consumable_dict", "r") as f:
        gv.consumable_dict = json.load(f)

# ----------------------------- GUI functions ----------------------------- #


def start(update, context):

    if not str(chatID(update)) in gv.character_dict.keys():

        update.message.reply_text(new_game_msg(),
                                  reply_markup=new_game_menu())

    else:
        update.message.reply_text(start_menu_msg(),
                                  reply_markup=start_game_menu())


def continue_(update, context):
    update.message.reply_text(main_menu_message(),
                              reply_markup=main_menu_keyboard())


def continue_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=main_menu_message(),
                            reply_markup=main_menu_keyboard())


def main_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=main_menu_message(),
                            reply_markup=main_menu_keyboard())


def moving_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=moving_message(),
                            reply_markup=moving_keyboard())


def image_test_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=image_test_msg(),
                            reply_markup=image_test_keyboard())


def exit_function(update, context):
    query = update.callback_query

    query.answer()

    query.edit_message_text(text="Ciao!")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def chatID(query):
    return str(query.message.chat.id)


def stop(bot, update):
    store_data()
    os.kill(os.getpid(), signal.SIGINT)

############################# Handlers #########################################


def main():

    initiation()

    updater = Updater(gv.bot_token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('weiter', continue_))
    updater.dispatcher.add_handler(CallbackQueryHandler(continue_menu, pattern='continue'))

    # ----------------------------- new game part ----------------------------- #

    updater.dispatcher.add_handler(CallbackQueryHandler(start_new_game, pattern='new_game'))
    updater.dispatcher.add_handler(CallbackQueryHandler(class_selection, pattern='(warrior)|(hunter)|(mage)'))
    updater.dispatcher.add_handler(conv_handler)

    # ----------------------------- playing part ----------------------------- #

    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))

    updater.dispatcher.add_handler(CallbackQueryHandler(moving_menu, pattern='move'))
    updater.dispatcher.add_handler(CallbackQueryHandler(general_info, pattern='info_main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(character_info, pattern='info_char'))
    updater.dispatcher.add_handler(CallbackQueryHandler(send_map, pattern='map'))
    updater.dispatcher.add_handler(CallbackQueryHandler(image_test_menu, pattern='test'))
    updater.dispatcher.add_handler(CallbackQueryHandler(relax_character, pattern='rest'))

    updater.dispatcher.add_handler(CallbackQueryHandler(move_the_character, pattern='(up)|(down)|(left)|(right)'))

    updater.dispatcher.add_handler(CallbackQueryHandler(exit_function, pattern='exit'))

    # --- Inventory management --- #
    updater.dispatcher.add_handler(CallbackQueryHandler(print_inventory, pattern='inventory'))
    updater.dispatcher.add_handler(CallbackQueryHandler(show_useables, pattern='show_useables'))
    updater.dispatcher.add_handler(CallbackQueryHandler(use_item, pattern='0[1-9]|10'))
    updater.dispatcher.add_handler(CallbackQueryHandler(delete_item, pattern='d0[1-9]|d10'))

    updater.dispatcher.add_handler(CommandHandler('kill_bot_lul_1337', stop))

    updater.start_polling()

    updater.idle()
################################################################################


if __name__ == '__main__':
    main()

    print(gv.character_dict)
