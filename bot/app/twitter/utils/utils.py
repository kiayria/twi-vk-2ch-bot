import tweepy

from cfg import config
from app import db


def get_twitter_auth():
    return tweepy.OAuthHandler(
        consumer_key=config.TWITTER_CONSUMER_KEY,
        consumer_secret=config.TWITTER_CONSUMER_SECRET
    )


def get_twitter_api(auth, chat_id):
    tokens = db.get_twitter_tokens(chat_id)
    if tokens is None:
        return None
    auth.set_access_token(
        tokens['token_key'],
        tokens['token_secret']
    )

    return tweepy.API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )
