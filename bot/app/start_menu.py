from app.utils.states import CHOOSING
from app.utils.keyboards import get_start_markup


def start_menu(update, context):
    update.message.reply_text(
        text='Hi there! Let`s waste some time.',
        reply_markup=get_start_markup()
    )

    return CHOOSING


# @dp.callback_query_handler(text='return', state='*')
# async def start_menu(query, state):
#     await query.answer()
#     await query.message.edit_text(
#         reply_markup=get_start_markup())


# @dp.message_handler(content_types=types.ContentTypes.ANY, state='*')
# async def unknown_command(message):
#     await message.reply('Эта команда мне неизвестна.')
