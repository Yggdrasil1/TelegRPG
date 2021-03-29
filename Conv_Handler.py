from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from Bot_Functions import *
from Keyboards import name_selection_success_keyboard, main_menu_keyboard
import global_variables as gv

# ----------------------------- Name selecting ----------------------------- #

CHOOSING = 1
FAIL = 2


def name_selection(update, context):
    query = update.callback_query

    query.edit_message_text("Bitte wähle einen Namen mit 3-20 Buchstaben und ohne Sonderzeichen:")

    return CHOOSING


def not_enough_letters(update, context):
    print(update.message.text)
    update.message.reply_text("Dein Name muss zwischen 3 und 20 Zeichen beinhalten " +\
                            "und sollte ohne Sonderzeichen auskommen")

    return CHOOSING


def enough_letters(update, context):

    name = update.message.text
    chatid = chatID(update)
    gv.character_dict[chatid].name = name
    update.message.reply_text("Check! Den nehmen wir so, bist du zufrieden mit {}?".format(name),
                            reply_markup=name_selection_success_keyboard())

    return FAIL


def choose_another_name(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Dann wähle bitte jetzt deinen Namen.")
    return CHOOSING


def chose_name_finally(update, context):

    query = update.callback_query
    query.answer()
    final_name = gv.character_dict[chatID(query)].name
    query.edit_message_text(f"Sehr gut, dann von mir ein Herzliches Willkommen {final_name}!"\
                            "\nDann lass uns jetzt eine Runde spielen. Learning by doing. Tipp: Tippe auf Info "\
                            "um dir anzeigen zu lassen was jeder Knopf im Hauptmenü macht. (Das Hauptmenü ist das was "\
                            f"gerade angezeigt wird " + u'\U0001F447' + ")",
                            reply_markup=main_menu_keyboard())

    print(gv.character_dict)

    return ConversationHandler.END


def exit_function(update, context):
    query = update.callback_query

    query.answer()

    query.edit_message_text(text="Ciao!")


conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(name_selection, pattern='select_name')],
        #per_message=True,

        states={
            CHOOSING: [MessageHandler(Filters.regex('^[A-Za-z]{3,20}$'),
                                      enough_letters),
                       MessageHandler(Filters.regex('^(?!([A-Za-z]{3,20}$))'),
                                      not_enough_letters)
                       ],

            FAIL: [CallbackQueryHandler(chose_name_finally, pattern='happy_name'),
                   CallbackQueryHandler(choose_another_name, pattern='sad_name')
                  ]


        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), exit_function)]
    )


def chatID(query):
    return str(query.message.chat.id)