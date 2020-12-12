from aiogram import types

from app import dp, Form
from app.utils.keyboards import get_start_markup, get_twi_markup


@dp.message_handler(commands='start', state='*')
async def cmd_start(message, state):
    await state.finish()
    await message.answer(
        text='Hi there! Let`s waste some time.',
        reply_markup=get_start_markup()
    )


@dp.callback_query_handler(text='twi_btn', state='*')
async def twi_menu(query, state):
    await query.answer()
    await Form.twitter.set()
    await query.message.edit_text(
        text='Функции твиттера',
        reply_markup=get_twi_markup()
    )


@dp.callback_query_handler(text='return', state='*')
async def start_menu(query, state):
    await query.answer()
    await query.message.edit_text(
        reply_markup=get_start_markup())


@dp.message_handler(content_types=types.ContentTypes.ANY, state='*')
async def unknown_command(message):
    await message.reply('Эта команда мне неизвестна.')
