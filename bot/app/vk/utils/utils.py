from app import db


def set_token(chat_id, token):
    db.save_vk_token(chat_id, token)


def get_token(chat_id):
    return db.get_vk_token(chat_id)


def remove_token(chat_id):
    db.remove_vk_token(chat_id)


def stat_text(chat_id, text):
    words = text.replace('\n', ' ').split(' ')
    unique_words = dict()
    for word in words:
        if word in unique_words:
            unique_words[word] += 1
        else:
            unique_words[word] = 1

    db.update_stat(chat_id, unique_words, 'vk')
