import tweepy
from telegram.ext import Updater

from cfg import config


updater = Updater(config.BOT_TOKEN, use_context=True)
dp = updater.dispatcher

twitter_auth = tweepy.OAuthHandler(
    consumer_key=config.TWITTER_CONSUMER_KEY,
    consumer_secret=config.TWITTER_CONSUMER_SECRET
)
twitter_auth.set_access_token(
    config.TWITTER_ACCESS_KEY,
    config.TWITTER_ACCESS_SECRET
)
api = tweepy.API(
    twitter_auth,
    wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True
)

from app.conversation import get_conversation


dp.add_handler(get_conversation())
