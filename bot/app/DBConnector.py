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
        if user is None or user['data']['twitter']['oauth_token'] == '' \
                or user['data']['twitter']['oauth_token_secret'] == '':
            return None

        return {
            'token_key': user['data']['twitter']['oauth_token'],
            'token_secret': user['data']['twitter']['oauth_token_secret']
        }

    def get_vk_token(self, chat_id):
        user = self.users.find_one({'chat_id': str(chat_id)})
        if user is None or user['data']['vk']['oauth_token'] == '':
            return None

        return {'token_key': user['data']['vk']['oauth_token']}

    def save_token(self, chat_id, token):
        self.users.find_one_and_update({
            'chat_id': str(chat_id)
        }, {
           '$set': {
               'data.twitter.oauth_token': token
           }
        })

    def remove_twitter_tokens(self, chat_id):
        self.users.find_one_and_update({
            'chat_id': str(chat_id)
        }, {
            '$set': {
                'data.twitter.oauth_token': '',
                'data.twitter.oauth_token_secret': '',
            }
        })

    def get_user(self, chat_id):
        return self.users.find_one({'chat_id': str(chat_id)})

    def update_stat(self, chat_id, words, api=None):
        if api not in ('twitter', 'vk', 'dvach'):
            return

        user = self.users.find_one({'chat_id': str(chat_id)})
        for word, count in words.items():
            if word in user['data'][api]['statistics']['words']:
                user['data'][api]['statistics']['words'][word] += count
            else:
                user['data'][api]['statistics']['words'][word] = count

        self.users.findOneAndReplace(
            {'chat_id': str(chat_id)},
            user
        )
