import tweepy
from aiogram import types

from app import dp, bot, api, twitter_auth
from app.MyListener import MyStreamListener
from app.utils.keyboards import get_twi_markup, get_start_markup
from app.utils.states import TwitterForm


@dp.callback_query_handler(text='twi_btn', state='*')
async def twi_menu(query, state):
    await query.answer()
    await query.message.edit_text(
        text='Функции твиттера',
        reply_markup=get_twi_markup()
    )


@dp.callback_query_handler(text='twi_login', state='*')
async def twi_login(query, state):
    await query.answer()
    # await query.message.edit_text(
    #     text='Here are twitter functions',
    #     reply_markup=get_twi_markup()
    # )
    await bot.send_message(query.from_user.id, str(twitter_auth.get_authorization_url()))


@dp.callback_query_handler(text='twi_tweet', state='*')
async def twi_tweet(query, state):
    await TwitterForm.tweet.set()
    await query.answer()
    await query.message.edit_text(
        text='Введите текст сообщения',
        reply_markup=get_twi_markup()
    )


@dp.message_handler(commands='twi_tweet', state='*')
async def cmd_start(message, state):
    user_text = str(message.text).replace('twi_tweet', '')
    await message.answer(
        text=f'Sent: {user_text}',
        reply_markup=get_twi_markup()
    )


@dp.message_handler(state=TwitterForm.tweet)
async def process_tweet(message, state):
    async with state.proxy() as data:
        # api = data['api']
        # api.update_status(str(message.text))

        # Create a tweet
        if len(message.text) < 140:
            api.update_status(message.text)
            await message.answer(
                text='Твит отправлен',
                reply_markup=get_twi_markup()
            )
        else:
            await message.answer(
                text='Ой! Слишком много букв!',
                reply_markup=get_twi_markup()
            )
    await state.finish()


@dp.callback_query_handler(text='twi_news', state='*')
async def twi_news(query, state):
    await TwitterForm.news.set()
    await query.answer()
    await query.message.edit_text(
        text='Секундочку... Откапываем твиты...',
    )
    timeline = api.home_timeline()
    txt = "Мы нашли эти твиты:\n"
    for tweet in timeline:
        txt += f"{tweet.user.name} говорит:\n {tweet.text}\n * * * * * * * * *\n\n\n"
    await bot.send_message(query.from_user.id, txt, reply_markup=get_twi_markup())


@dp.callback_query_handler(text='twi_stream', state='*')
async def twi_stream(query, state):
    await TwitterForm.stream.set()
    await query.answer()
    txt = "Что будем искать?"
    await bot.send_message(query.from_user.id, txt, reply_markup=get_twi_markup())


@dp.callback_query_handler(text='twi_stream_off', state=TwitterForm.stream)
async def twi_stream(query, state):
    with state.proxy() as data:
        stream = data.pop('stream', None)
        if stream is None:
            return
        stream.disconnect()
    await state.finish()


@dp.message_handler(state=TwitterForm.stream)
async def process_stream(message, state):
    await bot.send_message(
        chat_id=message.chat.id,
        text='Секундочку... Запускаем стрим...'
    )
    tags = str(message.text).split(' ')

    tweets_listener = MyStreamListener(
        api=api,
        bot=bot,
        chat_id=message.chat.id
    )
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=tags, languages=["en", "ru"], is_async=True)
    async with state.proxy() as data:
        data['stream'] = stream


@dp.callback_query_handler(text='return', state='*')
async def go_back_to_menu(query, state):
    await query.answer()
    await query.message.edit_text(
        text='Мы сделали шаг назад...',
        reply_markup=get_start_markup()
    )
