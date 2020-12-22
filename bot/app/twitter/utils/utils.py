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


def remove_tokens(chat_id):
    db.remove_twitter_tokens(chat_id)


def stat_text(chat_id, text):
    words = text.replace('\n', ' ').split(' ')
    unique_words = dict()
    for word in words:
        if word in unique_words:
            unique_words[word] += 1
        else:
            unique_words[word] = 1

    db.update_stat(chat_id, unique_words, 'twitter')
