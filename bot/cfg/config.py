import os


BOT_TOKEN = os.environ.get('BOT_TOKEN', '')
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', '')


MONGO_URI = 'mongodb://{user}:{passwd}@{host}:{port}'.format(
    user=os.environ.get('MONGO_INITDB_ROOT_USERNAME', 'admin'),
    passwd=os.environ.get('MONGO_INITDB_ROOT_PASSWORD', 'admin'),
    host=os.environ.get('MONGO_HOST', 'localhost'),
    port=os.environ.get('MONGO_PORT', '27017'),
)
