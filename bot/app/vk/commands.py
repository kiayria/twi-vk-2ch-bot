from app import api, twitter_auth
from app.vk.utils.keyboards import get_vk_markup
from app.utils.states import VK_DEFAULT, VK_POST, VK_STATUS

import vk_api


def vk_menu(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Функции ВК',
        reply_markup=get_vk_markup()
    )

    return VK_DEFAULT


def vk_login(update, context):

    #enter a login



    return VK_DEFAULT


def vk_change_status(update, context):
    # enter a status
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Введите статус',
        reply_markup=get_vk_markup()
    )

    return VK_STATUS


def vk_post(update, context):
    # enter a post text
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Введите статус',
        reply_markup=get_vk_markup()
    )

    return VK_POST


def vk_logout(update, context):

    return VK_DEFAULT


def process_status(update, context):
    status_text = update.message.text
    answer_text = 'Вы поставили статус:\n' + status_text
    #res = vk_api.VkApi(token=hardcode_token).get_api().status.set(text=status_text)

    update.message.reply_text(
        answer_text,
        reply_markup=get_vk_markup()
    )


    return VK_DEFAULT


def process_post(update, context):

    post_text = update.message.text
    answer_text = 'Запощено'

    vk_api.VkApi(token=hardcode_token).get_api().wall.post(text=post_text)

    update.message.reply_text(
        answer_text,
        reply_markup=get_vk_markup()
    )

    return VK_DEFAULT


#####################################

