from pymongo import MongoClient

from cfg import config


class DBConnector:
    def __init__(self):
        client = MongoClient(config.MONGO_URI)
        self.client = client
        self.users = client.test.users

    def init_user(self, chat_id):
        user = self.users.find_one({'chat_id': str(chat_id)})
        print(f'User is {user}')
        if user is None:
            self.users.insert_one(
                {
                    "chat_id": str(chat_id),
                    "data": {
                        "twitter": {
                            "oauth_token": "",
                            "oauth_token_secret": "",
                            "last_seen_id": "",
                            "username": "",
                            "statistics": {
                                "words": []
                            },
                        },
                        "vk": {
                            "oauth_token": "",
                            "statistics": {
                                "words": []
                            },
                        },
                        "dvach": {
                            "statistics": {
                                "words": []
                            }
                        },
                    },
                }
            )

    def get_twitter_tokens(self, chat_id):
        user = self.users.find_one({'chat_id': str(chat_id)})
        if user is None:
            return None

        return {
            'token_key': user.token_key,
            'token_secret': user.token_secret
        }

    def save_token(self, chat_id, token):
        self.users.find_one_and_update({
            'chat_id': str(chat_id)
        }, {
           '$set': {
               'data.twitter.oauth_token': token
           }
        }, upsert=True)
