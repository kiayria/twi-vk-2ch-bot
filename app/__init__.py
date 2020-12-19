from telegram.ext import Updater
import tweepy
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from cfg import config


updater = Updater(config.TOKEN, use_context=True)
dp = updater.dispatcher

from app.commands.conversation import get_conversation

dp.add_handler(get_conversation())

# bot = Bot(token=config.TOKEN)
# memory_storage = MemoryStorage()
# dp = Dispatcher(bot, storage=memory_storage)
# twitter_auth = tweepy.OAuthHandler(
#     consumer_key=config.TWITTER_CONSUMER_KEY,
#     consumer_secret=config.TWITTER_CONSUMER_SECRET
# )
# twitter_auth.set_access_token(
#     config.TWITTER_ACCESS_KEY,
#     config.TWITTER_ACCESS_SECRET
# )
# api = tweepy.API(
#     twitter_auth,
#     wait_on_rate_limit=True,
#     wait_on_rate_limit_notify=True
# )
#
# from app.utils.states import Form
#
# from app.commands import start_menu, twitter_menu
