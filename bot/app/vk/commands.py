import requests
import vk_api

from app.vk.utils.keyboards import VK_UNAUTHORIZED_MARKUP, VK_AUTHORIZED_MARKUP
from app.vk.utils.utils import set_token, remove_token, get_token, stat_text
from app.utils.states import VK_DEFAULT, VK_POST, VK_STATUS, VK_LOGIN
from cfg import config


PERMISSIONS = vk_api.VkUserPermissions.STATUS + vk_api.VkUserPermissions.WALL + vk_api.VkUserPermissions.OFFLINE


def vk_menu(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Функции ВК',
        reply_markup=VK_UNAUTHORIZED_MARKUP
    )

    return VK_DEFAULT


def vk_login(update, context):

    # building link
    uri = config.VK_REDIRECT_URI
    chat_id = str(update.effective_chat.id)
    link = f'https://oauth.vk.com/authorize?client_id=7705522&scope={PERMISSIONS}&redirect_uri={uri}&' \
           f'display=page&v=5.126&response_type=token&state={chat_id}'

    # get token
    access_token = ''

    answer_text = 'Авторизуйтесь по ссылке:\n' + link
    chat_id = str(update.effective_chat.id)

    context.bot.send_message(
        chat_id=chat_id,
        text=answer_text
    )

    return VK_LOGIN


def process_login_vk(update, context):

    chat_id = str(update.effective_chat.id)
    access_token = update.message.text

    set_token(
        chat_id=update.effective_chat.id,
        token=access_token
    )

    final_text = ''

    try:
        api = vk_api.VkApi(token=access_token).get_api()
        final_text = f'Вы вошли как  {api.users.get()[0]["first_name"]} {api.users.get()[0]["last_name"]}.'
    except vk_api.ApiError as err:
        final_text = 'Ошибка авторизации'

    context.bot.send_message(
        text=final_text,
        chat_id=update.effective_chat.id,
        reply_markup=VK_AUTHORIZED_MARKUP
    )

    return VK_DEFAULT


def vk_change_status(update, context):
    # enter a status
    query = update.callback_query
    query.answer()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите статус'
    )

    return VK_STATUS


def vk_post(update, context):
    # enter a post text
    query = update.callback_query
    query.answer()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Введите текст поста'
    )

    return VK_POST


def vk_logout(update, context):

    chat_id = str(update.effective_chat.id)
    remove_token(chat_id=update.effective_chat.id)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Ваш токен удалён'
    )

    return VK_DEFAULT


def process_status(update, context):
    status_text = update.message.text

    access_token = get_token(update.effective_chat.id)

    try:
        answer_text = 'Вы поставили статус:\n' + status_text
        vk_api.VkApi(token=access_token).get_api().status.set(text=status_text)
    except vk_api.ApiError as E:
        print(E)
        answer_text = 'Ошибка аутентификации. Попробуйте перезайти'

    update.message.reply_text(
        answer_text,
        reply_markup=VK_UNAUTHORIZED_MARKUP
    )

    return VK_DEFAULT


def process_post(update, context):
    post_text = update.message.text

    access_token = get_token(update.effective_chat.id)

    try:
        answer_text = 'Запощено'
        vk_api.VkApi(token=access_token).get_api().wall.post(message=post_text)
        stat_text(update.effective_chat.id, post_text)
    except vk_api.ApiError:
        answer_text = 'Ошибка аутентификации. Попробуйте перезайти'

    update.message.reply_text(
        answer_text,
        reply_markup=VK_AUTHORIZED_MARKUP
    )

    return VK_DEFAULT
