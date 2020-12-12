from aiogram import types

from app import dp, Form
from app.utils.keyboards import get_twi_markup


@dp.callback_query_handler(text='twi_login', state=Form.twitter)
async def twi_menu(query, state):
    await query.answer()
    await query.message.edit_text(
        text='Here are twitter functions',
        reply_markup=get_twi_markup()
    )


@dp.callback_query_handler(text='twi_tweet', state=Form.twitter)
async def twi_menu(query, state):
    await query.answer()
    await query.message.edit_text(
        text='Here are twitter functions',
        reply_markup=get_twi_markup()
    )

