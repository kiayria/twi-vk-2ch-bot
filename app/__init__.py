import tweepy
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from cfg import config

bot = Bot(token=config.TOKEN)
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)
twitter_auth = tweepy.OAuthHandler(
    consumer_key=config.TWITTER_CONSUMER_KEY,
    consumer_secret=config.TWITTER_CONSUMER_SECRET
)

from app.utils.states import Form

from app.commands import start_menu, twitter_menu
