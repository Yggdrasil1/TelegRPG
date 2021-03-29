from matplotlib import pyplot as plt
from matplotlib import transforms
from matplotlib import image as mpimg
import global_variables as gv

import matplotlib.patches as patches
import numpy
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Bot
from io import BytesIO
import numpy as np
import os
import logging


def send_image(bot, chatID, image_path, delete_image: bool = False):

    bot.sendPhoto(chatID,
                  photo=open(image_path, 'rb'))

    if os.path.exists(image_path) and delete_image:
        os.remove(image_path)

    return


def create_map_image(x_coord, y_coord, chatid):

    fig, ax = plt.subplots(1)

    img = mpimg.imread(gv.temp_images + "world.png")

    img_plot = plt.imshow(img)

    plt.axis('off')

    my_marker = plt.scatter(x_coord, y_coord, s=120, c='white', marker='x', edgecolors="white", linewidth=8)
    my_marker2 = plt.scatter(x_coord, y_coord, s=70, c='black', marker='x', edgecolors="white", linewidth=3)
    ax.add_artist(my_marker)
    ax.add_artist(my_marker2)

    #base = plt.gca().transData
    #rot = transforms.Affine2D().rotate_deg(180)

    #print(img.shape)

    #ax.set_transform(rot+base)

    image_name = gv.temp_images + "world" + str(chatid) + ".png"

    plt.savefig(image_name, dpi=800)

    return image_name


def create_item_image(item_name, stats, chatid):
    atak = stats[0]
    defe = stats[1]
    stre = stats[2]
    dext = stats[3]
    inte = stats[4]

    print(gv.temp_images + item_name + ".png")

    img = mpimg.imread(gv.temp_images + item_name + ".png")

    fig, ax = plt.subplots(1)

    imgplot = plt.imshow(img)

    plt.text(255, 30, f"ATK = {atak}", size=13, family="fantasy", weight='bold')
    plt.text(255, 80, f"DEF = {defe}", size=13, family="fantasy", weight='bold')
    plt.text(255, 130, f"STR = {stre}", size=13, family="fantasy", weight='bold')
    plt.text(255, 180, f"DEX = {dext}", size=13, family="fantasy", weight='bold')
    plt.text(255, 230, f"INT = {inte}", size=13, family="fantasy", weight='bold')
    # plt.text(255, 40, f"DEF = {defe}", size=13, family="fantasy", weight='bold')

    plt.axis('off')

    image_name = gv.temp_images + "item" + str(chatid) + ".png"

    plt.savefig(image_name, dpi=800)

    return image_name
