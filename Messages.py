import Gear
import global_variables as gv
import Character

# ----------------------------- Messages ----------------------------- #


def main_menu_message():
    return 'Was möchtest du tun?'


def moving_message():
    return 'In welche Richtung möchtest du gehen?:'


def next_action_message():
    return 'Was möchtest du als nächstes tun?:'


def image_test_msg():
    return 'Wähle eine Form.'


def start_menu_msg():
    return_string = 'Hey, wie es aussieht haben wir bereits einen Charakter von dir im System ' + \
                    'willst du mit diesen Charakter fortsetzen? ' + \
                    'Ansonsten kannst du hier deinen Charakter resetten.'

    return return_string


def new_game_msg():
    return_string = 'Es sieht aus als wärst du neu hier. Willkommen! \n' + \
                    'Drück "Start" um einen neuen Charakter anzulegen \n' + \
                    'Falls du das nicht möchtest drück Beenden um den Bot wieder zu verlassen.'

    return return_string


def class_selection_msg():
    return_string = 'Bitte wähle nun eine Klasse. Da es eigentlich keinen \n' + \
                    'Unterschied macht welcher Klasse dein Charakter angehört \n' + \
                    'nimm am Besten was du am coolsten findest :D.'

    return return_string


def class_selected_msg(class_string):
    return_string = 'Du hast dich also für eine/einen {}In entschieden \n' + \
                    '(Geschlechter machen hier keinen Unterschied).'

    return return_string


def name_selection_msg():
    return_string = 'Bevor es losgeht würde ich noch gerne wissen wie ich und andere dich ' +\
                    'nennen sollen. Im nächsten Schritt kannst du deinen Namen wählen.'

    return return_string


def inventory_msg(inventory):
    helmet = inventory["Helmet"]
    chest = inventory["Chest"]
    pants = inventory["Pants"]
    boots = inventory["Boots"]
    weapon = inventory["Weapon"]

    return_string = f'{"Atk":<3} {"Def":<3} {"Str":<3} {"Dex":<3} {"Int":<3} {"Name"}\n' + \
                    Gear.format_item_text(weapon) + \
                    Gear.format_item_text(helmet) +\
                    Gear.format_item_text(chest) + \
                    Gear.format_item_text(pants) + \
                    Gear.format_item_text(boots)

    return return_string


def world_border_reached_msg():

    return_string = "Ah, du hast leider die Grenzen der derzeitigen Welt erreicht. Bitte wähle eine andere Richtung"

    return return_string


def movement_msg(direction, region, old_region, x, y):

    return_string = f' Du läuft Richtung {gv.himmelsrichtungen[direction]} [{x}, {y}]. \n'

    if region != old_region:
        return_string += f'Du bist jetzt {gv.regions_dict[region]}.'

    return return_string


def water_reached_msg():

    return_string = "Da ist Wasser. Leider kannst du nicht weiter in diese Richtung, bitte wähle eine andere."

    return return_string


def monster_spawn_msg(monster_name):

    return_string = f"Oh, Oh!! {monster_name} greift dich an!"

    return return_string


def you_died_msg():

    return_string = f"Du wurdest besiegt und man hielt dich für tot. Du wachst auf dem Friedhof [50, 67] auf."

    return return_string


def map_msg(region):

    return_string = f"Du befindest dich {gv.regions_dict[region]}"

    return return_string


def info_main_msg():

    return_string = f"Die Funktion aller Menüknöpfe im Hauptmenü: \n" \
                    f"------------------------------------------ \n \n" \
                    f"BEWEGEN: Erlaubt es dir dich in der Welt zu bewegen, " \
                    f"schau auf die Karte um zu sehen wo du bist. \n \n" \
                    f"AUSRUHEN: Heilt dich, du kannst dich aber eine Weile nicht bewegen oder Items benutzen. \n \n" \
                    f"CHARAKTER: Zeigt dir Informationen über deinen Charakter... duh. \n \n" \
                    f"KARTE: Sendet dir ein Bild der Welt mit deinem aktuellen Standort als X. \n \n" \
                    f"INVENTAR: Zeigt dir die Stats deiner derzeitigen Ausrüstung und " \
                    f"erlaubt dir alle Items die du nicht " \
                    f"trägst zu benutzen oder anzuziehen (je nach Item). \n \n" \
                    f"INFO: ... Kriegste selber raus, ne? \n\n" \
                    f"BEENDEN: Schließt alle Menüs. Du kannst das Spiel wieder starten mit '/start'. "

    return return_string


def character_info_msg(character):

    return_string = f"Dein Charakter im Überblick: \n" \
                    f"----------------------------------- \n\n" \
                    f"{character.character_description()}"

    return return_string


def lvl_up_msg(character):

    main_stat_list = {'warrior': [1, 0, 0],
                      'hunter': [0, 1, 0],
                      'mage': [0, 0, 1]}

    return_string = f"LVL up! Neues lvl: -- {character.lvl} -- \n\n" \
                    f"Stärke: +{1 + main_stat_list[character.klasse][0]} \n" \
                    f"Geschicklichkeit: +{1 + main_stat_list[character.klasse][1]} \n" \
                    f"Intelligenz: +{1+ main_stat_list[character.klasse][2]} \n\n" \
                    f"Max HP: +2"

    return return_string


def item_added_to_inv_msg(slot, item_name):

    return_string = f"Das Item '{item_name}' wurde zu deinem Inventar hinzugefügt an Platz: {slot}."

    return return_string