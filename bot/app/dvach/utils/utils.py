from app import db


def stat_text(chat_id, text):
    words = text.replace('\n', ' ').split(' ')
    unique_words = dict()
    for word in words:
        if word in unique_words:
            unique_words[word] += 1
        else:
            unique_words[word] = 1

    db.update_stat(chat_id, unique_words, 'twitter')