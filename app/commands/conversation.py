from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler
from . import CHOOSING, TWITTER_DEFAULT, TWITTER_TWEET, TWITTER_STREAM, VK, DVACH
from .start_menu import start_menu
from .twitter_menu import twi_menu, twi_tweet


def get_conversation():
    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start_menu)],
        states={
            CHOOSING: [
                CallbackQueryHandler(twi_menu, pattern='^twi_btn$'),
                CallbackQueryHandler(twi_menu, pattern='^vk_btn$'),
            ],
            TWITTER_DEFAULT: [
                CallbackQueryHandler(twi_menu, pattern='^twi_login$'),
                CallbackQueryHandler(twi_tweet, pattern='^twi_tweet$'),

            ],
            VK: [],
            DVACH: []
        },
        fallbacks=[]
    )

    return conv
