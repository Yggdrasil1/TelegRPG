# ----------------------------- The Bot ----------------------------- #
from telegram import Bot


with open("D://Programme//telegram_bot//bot_token.txt") as f:
    for line in f:
        bot_token = line

bot = Bot(bot_token)

# ----------------------------- Dictionaries ----------------------------- #

player_dict = {}

# ChatId: Character
character_dict = {}

# ChatId: Inventory
inventory_dict = {}

# Name-part: Rarity: Item_type
item_name_dict = {}

# X: Y: Region
world_map = {}

# X: Y: Monster_lvl
monster_lvl_dict = {}

# int(lvl): str(Name): int(rarity [1,2]): list(attributes)
monster_name_dict = {}

# Direction: [+/- X, +/- Y]
direction_dict = {}

# Region: german description
regions_dict = {}

# Direction: german direction
himmelsrichtungen = {}

# lvl: exp needed
lvl_dict = {}

# consumable name: heal ratio
consumable_dict = {}

# klasse: main stat
main_stat_dict = {'warrior': 'strength',
                  'hunter': 'dexterity',
                  'mage': 'intelligence'}

#dict to handle item destruction
destroy_item_dict = {}

# ----------------------------- Debug Bools ----------------------------- #


character_debug: bool = True

# ----------------------------- Paths ----------------------------- #

character_path = "D:\\Programme\\telegram_bot\\Character_data\\Character\\"
inventory_path = "D:\\Programme\\telegram_bot\\Character_data\\Inventory\\"
temp_images = 'D:\\Programme\\telegram_bot\\Temp_images\\'
img_folder = 'D:\\Programme\\telegram_bot\\Item_imgs\\'
item_names_path = 'D:\\Programme\\RPG\\StreamRPG\\'
world_map_path = "D:\\Programme\\RPG\\StreamRPG\\map.csv"
monster_lvl_path = "D:\\Programme\\RPG\\StreamRPG\\lvl.csv"
monster_name_path = "D:\\Programme\\telegram_bot\\Mob_names\\monster_name_dict"

# ----------------------------- World borders ----------------------------- #

world_max_x = 0
world_max_y = 0

# ----------------------------- Fighting Parameter ----------------------------- #

dodge_beta_value = 3
