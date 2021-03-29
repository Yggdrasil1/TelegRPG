
# ----------------------------- Imports ----------------------------- #
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# ----------------------------- Keyboards ----------------------------- #


def main_menu_keyboard():
    keyboard = [
                [InlineKeyboardButton('Bewegung', callback_data='move'),
                 InlineKeyboardButton('Ausruhen', callback_data='rest'),
                 InlineKeyboardButton('Charakter', callback_data='info_char')],

                [InlineKeyboardButton('Karte', callback_data='map'),
                 InlineKeyboardButton('Inventar', callback_data='inventory'),
                 InlineKeyboardButton('x', callback_data='ssp')],

                [InlineKeyboardButton('x', callback_data='Arena'),
                 InlineKeyboardButton('Info', callback_data='info_main'),
                 InlineKeyboardButton('Beenden', callback_data='exit')]
               ]

    return InlineKeyboardMarkup(keyboard)


def moving_keyboard():
    keyboard = [
                [InlineKeyboardButton('Norden [y-1]', callback_data='up')],

                [InlineKeyboardButton('Westen [x-1]', callback_data='left'),
                 InlineKeyboardButton('Osten [x+1]', callback_data='right')],

                [InlineKeyboardButton('Süden [y+1]', callback_data='down')],

                [InlineKeyboardButton('Hauptmenü', callback_data='main')]
               ]

    return InlineKeyboardMarkup(keyboard)


def image_test_keyboard():
    keyboard = [
                    [InlineKeyboardButton('Viereck', callback_data='square')],
                    [InlineKeyboardButton('Kreis', callback_data='circle')],
                    [InlineKeyboardButton('Hauptmenü', callback_data='main')]
               ]

    return InlineKeyboardMarkup(keyboard)


def start_game_menu():
    keyboard = [
                    [InlineKeyboardButton('Weitermachen', callback_data='continue')],
                    [InlineKeyboardButton('Neuer Character', callback_data='new_char')]
               ]

    return InlineKeyboardMarkup(keyboard)


def new_game_menu():
    keyboard = [
                    [InlineKeyboardButton('Starte ein neues Spiel', callback_data='new_game')],
                    [InlineKeyboardButton('Beenden', callback_data='exit')]
               ]

    return InlineKeyboardMarkup(keyboard)


def class_selection_keyboard():
    keyboard = [
                    [InlineKeyboardButton("Krieger", callback_data='warrior')],
                    [InlineKeyboardButton("Jäger", callback_data='hunter')],
                    [InlineKeyboardButton("Magier", callback_data='mage')],
                    [InlineKeyboardButton("Beenden", callback_data='exit')]
    ]

    return InlineKeyboardMarkup(keyboard)


def name_selection_keyboard():
    keyboard = [
                    [InlineKeyboardButton("Weiter", callback_data='select_name')],
                    [InlineKeyboardButton('Beenden', callback_data='exit')]
    ]

    return InlineKeyboardMarkup(keyboard)


def name_selection_success_keyboard():
    keyboard = [
                    [InlineKeyboardButton('Bin zufrieden', callback_data='happy_name')],
                    [InlineKeyboardButton('Nee, ich will doch nen anderen Namen', callback_data='sad_name')]
    ]

    return InlineKeyboardMarkup(keyboard)


def inventory_keyboard():
    keyboard = [
                    [InlineKeyboardButton('Zeige das Inventar', callback_data='show_useables')],
                    [InlineKeyboardButton('Hauptmenü', callback_data='main')]
    ]

    return InlineKeyboardMarkup(keyboard)


def useable_inventory(inventory):
    keyboard = []

    for slot in inventory.inv:

        if "not_eq" in slot:
            if hasattr(inventory.inv[slot], 'displayed_name'):
                displayed_name = inventory.inv[slot].displayed_name
            elif hasattr(inventory.inv[slot], 'name'):
                displayed_name = inventory.inv[slot].name
            else:
                displayed_name = inventory.inv[slot]

            keyboard.append([InlineKeyboardButton(f'{slot[-2:]}: {displayed_name}', callback_data=f'{slot[-2:]}')])

    keyboard.append([InlineKeyboardButton('Hauptmenü', callback_data='main')])

    return InlineKeyboardMarkup(keyboard)


def delete_item_keyboard(inventory):
    keyboard = []

    for slot in inventory.inv:

        if "not_eq" in slot:
            if hasattr(inventory.inv[slot], 'displayed_name'):
                displayed_name = inventory.inv[slot].displayed_name
            elif hasattr(inventory.inv[slot], 'name'):
                displayed_name = inventory.inv[slot].name
            else:
                displayed_name = inventory.inv[slot]

            keyboard.append([InlineKeyboardButton(f'{slot[-2:]}: {displayed_name}', callback_data=f'd{slot[-2:]}')])

    keyboard.append([InlineKeyboardButton('Zerstöre gefundenes Item', callback_data='pass')])

    return InlineKeyboardMarkup(keyboard)