import tweepy

from app.MyListener import MyStreamListener
from app import twitter_auth
from app.utils.keyboards import get_twi_markup
from . import TWITTER_DEFAULT, TWITTER_TWEET


def twi_menu(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Функции твиттера',
        reply_markup=get_twi_markup()
    )

    return TWITTER_DEFAULT


def twi_login(update, context):
    query = update.callback_query
    query.answer()

    job = context.job
    context.bot.send_message(job.context, text=str(twitter_auth.get_authorization_url()))


def twi_tweet(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Введите текст сообщения',
        reply_markup=get_twi_markup()
    )

    return TWITTER_TWEET


def process_tweet(update, context):
    text = update.message.text
    if len(text) < 140:
        api.update_status(text)
        answer_text = 'Твит отправлен'
    else:
        answer_text = 'Ой! Слишком много букв!'

    update.message.reply_text(
        answer_text,
        reply_markup=get_twi_markup()
    )

    return TWITTER_DEFAULT


def twi_news(update, context):


#
#
# @dp.callback_query_handler(text='twi_news', state='*')
# async def twi_news(query, state):
#     await TwitterForm.news.set()
#     await query.answer()
#     await query.message.edit_text(
#         text='Секундочку... Откапываем твиты...',
#     )
#     timeline = api.home_timeline()
#     txt = "Мы нашли эти твиты:\n"
#     for tweet in timeline:
#         txt += f"{tweet.user.name} говорит:\n {tweet.text}\n * * * * * * * * *\n\n\n"
#     await bot.send_message(query.from_user.id, txt, reply_markup=get_twi_markup())
#
#
# @dp.callback_query_handler(text='twi_stream', state='*')
# async def twi_stream(query, state):
#     await TwitterForm.stream.set()
#     await query.answer()
#     txt = "Что будем искать?"
#     await bot.send_message(query.from_user.id, txt, reply_markup=get_twi_markup())
#
#
# @dp.callback_query_handler(text='twi_stream_off', state=TwitterForm.stream)
# async def twi_stream(query, state):
#     with state.proxy() as data:
#         stream = data.pop('stream', None)
#         if stream is None:
#             return
#         stream.disconnect()
#     await state.finish()
#
#
# @dp.message_handler(state=TwitterForm.stream)
# async def process_stream(message, state):
#     await bot.send_message(
#         chat_id=message.chat.id,
#         text='Секундочку... Запускаем стрим...'
#     )
#     tags = str(message.text).split(' ')
#
#     tweets_listener = MyStreamListener(
#         api=api,
#         bot=bot,
#         chat_id=message.chat.id
#     )
#     stream = tweepy.Stream(api.auth, tweets_listener)
#     stream.filter(track=tags, languages=["en", "ru"], is_async=True)
#     async with state.proxy() as data:
#         data['stream'] = stream
#
#
# @dp.callback_query_handler(text='return', state='*')
# async def go_back_to_menu(query, state):
#     await query.answer()
#     await query.message.edit_text(
#         text='Мы сделали шаг назад...',
#         reply_markup=get_start_markup()
#     )
