from app import db


def set_token(chat_id, token):
    db.save_vk_token(chat_id, token)


def get_token(chat_id):
    return db.get_vk_token(chat_id)


def remove_token(chat_id):
    db.remove_vk_token(chat_id)
