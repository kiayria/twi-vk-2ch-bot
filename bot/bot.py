# from app import updater
from telegram.ext import Updater

from cfg import config
from app.conversation import get_conversation


def main():
    updater = Updater(config.BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(get_conversation())
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
