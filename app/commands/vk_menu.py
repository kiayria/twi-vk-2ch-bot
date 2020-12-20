from app import api, twitter_auth
from app.utils.keyboards import get_vk_markup
from . import VK_DEFAULT, VK_POST, VK_STATUS


def vk_menu(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Функции твиттера',
        reply_markup=get_vk_markup()
    )

    return VK_DEFAULT


def vk_login(update, context):
    pass


def vk_change_status(update, context):
    pass


def vk_post(update, context):
    pass


def vk_logout(update, context):
    pass
