import tweepy
from time import sleep

from app import db
from app.twitter.MyStreamListener import MyStreamListener
from app.twitter.utils.utils import get_twitter_auth, get_twitter_api, remove_tokens, stat_text
from app.twitter.utils.keyboards import (
    TWITTER_UNAUTHORIZED_MARKUP,
    TWITTER_AUTHORIZED_MARKUP,
    TWITTER_STREAM_MARKUP
)
from app.utils.states import (
    TWITTER_DEFAULT,
    TWITTER_TWEET,
    TWITTER_STREAM
)


def choose_keyboard(context):
    if context.user_data['twitter_logged_in']:
        return TWITTER_AUTHORIZED_MARKUP
    else:
        return TWITTER_UNAUTHORIZED_MARKUP


def twi_menu(update, context):
    query = update.callback_query
    query.answer()

    twitter_auth = get_twitter_auth()
    context.user_data['twitter_auth'] = twitter_auth
    twitter_api = get_twitter_api(twitter_auth, update.effective_chat.id)
    logged_in = True if twitter_api else False
    context.user_data['twitter_logged_in'] = logged_in
    context.user_data['twitter_api'] = twitter_api if twitter_api else None

    query.edit_message_text(
        text='Функции твиттера',
        reply_markup=choose_keyboard(context)
    )

    return TWITTER_DEFAULT


def twi_login(update, context):
    query = update.callback_query
    query.answer()

    twitter_auth = context.user_data['twitter_auth']
    link = str(twitter_auth.get_authorization_url())
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'Пройдите по ссылке и нажмите "Авторизовать": {link}'
    )
    oauth_token = link.split('=')[-1]
    db.save_token(chat_id=update.effective_chat.id, token=oauth_token)

    step = 0.2
    secs = 0
    while secs < 60:
        twitter_api = get_twitter_api(twitter_auth, update.effective_chat.id)
        if twitter_api:
            context.user_data['twitter_logged_in'] = True
            context.user_data['twitter_api'] = twitter_api
            query.edit_message_text(
                text='Успешно',
                reply_markup=choose_keyboard(context)
            )
            break

        secs += step
        sleep(step)
    else:
        query.edit_message_text(
            text='Ошибка',
            reply_markup=choose_keyboard(context)
        )

    return TWITTER_DEFAULT


def twi_tweet(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Введите текст сообщения',
        reply_markup=choose_keyboard(context)
    )

    return TWITTER_TWEET


def process_tweet(update, context):

    if not context.user_data['twitter_logged_in']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Нужна авторизация!'
        )
    else:
        text = update.message.text
        if len(text) < 140:
            stat_text(update.effective_chat.id, text)
            context.user_data['twitter_api'].update_status(text)
            answer_text = 'Твит отправлен'
        else:
            answer_text = 'Ой! Слишком много букв!'

        update.message.reply_text(
            answer_text,
            reply_markup=choose_keyboard(context)
        )

    return TWITTER_DEFAULT


def twi_news(update, context):
    query = update.callback_query
    query.answer()

    if not context.user_data['twitter_logged_in']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Нужна авторизация!'
        )
    else:
        query.edit_message_text(
            text="Секундочку... Откапываем твиты...",
            reply_markup=choose_keyboard(context)
        )

        twitter_api = context.user_data['twitter_api']
        timeline = twitter_api.home_timeline()
        txt = "Мы нашли эти твиты:\n"
        for tweet in timeline:
            txt += f"{tweet.user.name} говорит:\n {tweet.text}\n * * * * * * * * *\n\n\n"

        context.bot.send_message(
            update.effective_chat.id,
            text=txt,
            reply_markup=choose_keyboard(context)
        )
    return TWITTER_DEFAULT


def twi_stream(update, context):
    query = update.callback_query
    query.answer()

    if not context.user_data['twitter_logged_in']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Нужна авторизация!'
        )
        return TWITTER_DEFAULT

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Что будем искать?'
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
        reply_markup=choose_keyboard(context)
    )

    return TWITTER_DEFAULT


def process_stream(update, context):
    if not context.user_data['twitter_logged_in']:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Нужна авторизация!'
        )
        return TWITTER_DEFAULT

    twitter_api = context.user_data['twitter_api']
    text = update.message.text

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


def twi_logout(update, context):
    query = update.callback_query
    query.answer()

    remove_tokens(update.effective_chat.id)
    context.user_data['twitter_logged_in'] = False
    context.user_data['twitter_auth'] = None
    context.user_data['twitter_api'] = None
    query.edit_message_text(
        text='Успешно',
        reply_markup=choose_keyboard(context)
    )

    return TWITTER_DEFAULT
