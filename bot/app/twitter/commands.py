import tweepy

from app import db
from app.twitter.MyStreamListener import MyStreamListener
from app.twitter.utils.utils import get_twitter_auth, get_twitter_api
from app.twitter.utils.keyboards import TWITTER_MARKUP, TWITTER_STREAM_MARKUP
from app.utils.states import TWITTER_DEFAULT, TWITTER_TWEET, TWITTER_STREAM


def twi_menu(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Функции твиттера',
        reply_markup=TWITTER_MARKUP
    )
    twitter_auth = get_twitter_auth()
    context.user_data['twitter_auth'] = twitter_auth
    # twitter_api = get_twitter_api(twitter_auth, update.effective_chat.id)
    # if twitter_api is not None:
    #     context.user_data['twitter_api'] = twitter_api

    return TWITTER_DEFAULT


def twi_login(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Пройдите по ссылке и нажмите "Авторизовать"',
        reply_markup=TWITTER_MARKUP
    )
    twitter_auth = context.user_data['twitter_auth']
    link = str(twitter_auth.get_authorization_url())
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=link
    )
    print(link)
    oauth_token = link.split('=')[-1]
    db.save_token(chat_id=update.effective_chat.id, token=oauth_token)

    return TWITTER_DEFAULT


def twi_tweet(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Введите текст сообщения',
        reply_markup=TWITTER_MARKUP
    )

    return TWITTER_TWEET


def process_tweet(update, context):
    twitter_api = get_twitter_api(
        context.user_data['twitter_auth'],
        update.effective_chat.id
    )

    if twitter_api is None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Нужна авторизация!'
        )
        return TWITTER_DEFAULT

    text = update.message.text
    if len(text) < 140:
        twitter_api.update_status(text)
        answer_text = 'Твит отправлен'
    else:
        answer_text = 'Ой! Слишком много букв!'

    update.message.reply_text(
        answer_text,
        reply_markup=TWITTER_MARKUP
    )

    return TWITTER_DEFAULT


def twi_news(update, context):
    query = update.callback_query
    query.answer()

    twitter_api = get_twitter_api(
        context.user_data['twitter_auth'],
        update.effective_chat.id
    )
    if twitter_api is None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Нужна авторизация!'
        )
        return TWITTER_DEFAULT
    query.edit_message_text(
        text="Секундочку... Откапываем твиты...",
        reply_markup=TWITTER_MARKUP
    )

    timeline = twitter_api.home_timeline()
    txt = "Мы нашли эти твиты:\n"
    for tweet in timeline:
        txt += f"{tweet.user.name} говорит:\n {tweet.text}\n * * * * * * * * *\n\n\n"

    context.bot.send_message(
        update.effective_chat.id,
        text=txt,
        reply_markup=TWITTER_MARKUP
    )
    return TWITTER_DEFAULT


def twi_stream(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text="Что будем искать?",
        reply_markup=TWITTER_MARKUP
    )
    return TWITTER_STREAM


def twi_stream_off(update, context):
    query = update.callback_query
    query.answer()

    stream = context.user_data.pop('stream', None)
    if stream is None:
        return

    stream.disconnect()

    query.edit_message_text(
        text="Стрим закончен",
        reply_markup=TWITTER_MARKUP
    )

    return TWITTER_DEFAULT


def process_stream(update, context):
    text = update.message.text
    twitter_api = get_twitter_api(
        context.user_data['twitter_auth'],
        update.effevtive_chat.id
    )
    if twitter_api is None:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Нужна авторизация!'
        )
        return TWITTER_DEFAULT

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Секундочку... Запускаем стрим...',
        reply_markup=TWITTER_STREAM_MARKUP
    )
    tags = str(text).split(' ')

    tweets_listener = MyStreamListener(
        api=twitter_api,
        bot=context.bot,
        chat_id=update.effective_chat.id
    )
    stream = tweepy.Stream(twitter_api.auth, tweets_listener)
    stream.filter(track=tags, languages=["en", "ru"], is_async=True)
    context.user_data['stream'] = stream

    return TWITTER_STREAM
