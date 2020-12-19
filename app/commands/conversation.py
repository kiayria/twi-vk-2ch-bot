from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler
from . import CHOOSING, TWITTER, VK, DVACH
from .start_menu import start_menu
from .twitter_menu import twi_menu


def get_conversation():
    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start_menu)],
        states={
            CHOOSING: [
                CallbackQueryHandler(twi_menu, pattern='^twi_btn$'),
            ],
            TWITTER: [],
            VK: [],
            DVACH: []
        },
        fallbacks=[]
    )

    return conv
