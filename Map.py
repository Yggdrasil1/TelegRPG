import global_variables as gv
import numpy as np


def initiate_world():

    with open(gv.world_map_path, 'r') as inf:
        for line in inf:
            spl = line.split('\t')
            x_coord = int(spl[0])
            y_coord = int(spl[1])
            region = spl[2].strip()
            if x_coord not in gv.world_map:
                gv.world_map[x_coord] = {}
                gv.world_map[x_coord][y_coord] = region
            else:
                if y_coord not in gv.world_map[x_coord]:
                    gv.world_map[x_coord][y_coord] = region

    gv.world_max_x = np.amax(list(gv.world_map.keys()))
    gv.world_map_y = np.amax(list(gv.world_map[0].keys()))

    gv.direction_dict = {'up': [0, -1],
                      'down': [0, 1],
                      'left': [-1, 0],
                      'right': [1, 0]
                      }

    gv.regions_dict = {'beach': 'am Strand',
                       'dark_forest': 'im Düsterwald',
                       'dark_lands': 'in den dunklen Landen',
                       'dungeon_entry': 'vor einer Höhle',
                       'forest': 'im {}{} Wald {}{}'.format(u"\U0001F333", u"\U0001F333", u"\U0001F333", u"\U0001F333"),
                       'graveyard': 'auf dem Friedhof',
                       'mountains': 'im Gebirge',
                       'plains': 'in einer Graslandschaft',
                       'savanna': 'in der Savanne',
                       'town': 'in einer Stadt',
                       'water': 'im Meer'}

    gv.himmelsrichtungen = {'up': 'Norden',
                            'down': 'Süden',
                            'left': 'Westen',
                            'right': 'Osten'}

    with open(gv.monster_lvl_path, 'r') as inf:
        for line in inf:
            spl = line.split('\t')
            x_coord = int(spl[0])
            y_coord = int(spl[1])
            level = int(spl[2].strip())
            if x_coord not in gv.monster_lvl_dict:
                gv.monster_lvl_dict[x_coord] = {}
                gv.monster_lvl_dict[x_coord][y_coord] = level
            else:
                if y_coord not in gv.monster_lvl_dict[x_coord]:
                    gv.monster_lvl_dict[x_coord][y_coord] = level




