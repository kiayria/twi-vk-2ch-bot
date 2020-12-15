from aiogram import types

from app import dp, bot, Form, twitter_auth
from app.utils.keyboards import get_twi_markup


@dp.callback_query_handler(text='twi_btn', state='*')
async def twi_menu(query, state):
    await query.answer()
    await Form.twitter.set()
    await query.message.edit_text(
        text='Функции твиттера',
        reply_markup=get_twi_markup()
    )


@dp.callback_query_handler(text='twi_login', state=Form.twitter)
async def twi_login(query, state):
    await query.answer()
    # await query.message.edit_text(
    #     text='Here are twitter functions',
    #     reply_markup=get_twi_markup()
    # )
    await bot.send_message(query.from_user.id, str(twitter_auth.get_authorization_url()))


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('twi_tweet'), state=Form.twitter)
async def twi_tweet(query, state):
    user_text = str(query.data).replace('twi_tweet', '')
    await query.answer(text=user_text)
    await query.message.edit_text(
        text='Here are twitter functions',
        reply_markup=get_twi_markup()
    )


@dp.message_handler(commands='twi_tweet', state=Form.twitter)
async def cmd_start(message, state):
    user_text = str(message.text).replace('twi_tweet', '')
    await message.answer(
        text=f'Sent: {user_text}',
        reply_markup=get_twi_markup()
    )

