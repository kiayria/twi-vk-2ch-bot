import tweepy
from app.twitter.utils.keyboards import TWITTER_STREAM_MARKUP


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id
        self.me = api.me()

    def on_status(self, tweet):
        tweet_text = f'{tweet.user.name}:{tweet.text}'
        print(f"{tweet.user.name}:{tweet.text}")
        self.bot.send_message(
            chat_id=self.chat_id,
            text=tweet_text,
            reply_markup=TWITTER_STREAM_MARKUP
        )

    def on_error(self, status):
        print("Error detected")
