from app import dp, bot
from app.utils.keyboards import get_vk_markup


@dp.callback_query_handler(text='vk_btn', state='*')
async def vk_menu(query, state):
    await query.answer()
    await query.message.edit_text(
        text='Функции ВК',
        reply_markup=get_vk_markup()
    )
