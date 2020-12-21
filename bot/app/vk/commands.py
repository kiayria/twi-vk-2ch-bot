from app import api, twitter_auth
from app.vk.utils.keyboards import get_vk_markup
from app.utils.states import VK_DEFAULT, VK_POST, VK_STATUS

import vk_api

from pymongo import MongoClient


client = MongoClient('mongodb://admin:admin@localhost:27017')
db = client.test
collection = db.users

# FOR ACQUIRING TOKEN
PERMISSIONS = vk_api.VkUserPermissions.STATUS + vk_api.VkUserPermissions.WALL + vk_api.VkUserPermissions.OFFLINE
REDIRECT_URI = 'https://oauth.vk.com/blank.hmtl'

HARDCODE_TOKEN = '77a0e7da7d5583c180f24d734789c83ff62bc8b339b9986fa2652b32dc74031770943472f3c7c6df0bb5d'


def vk_menu(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Функции ВК',
        reply_markup=get_vk_markup()
    )

    return VK_DEFAULT


def vk_login(update, context):

    # building link
    link = 'https://oauth.vk.com/authorize?client_id=7705522&scope={PERMISSIONS}&redirect_uri={REDIRECT_URI}&display=page&v=5.126&response_type=token' \
        .format(PERMISSIONS=PERMISSIONS, REDIRECT_URI=REDIRECT_URI)

    # get token
    access_token = ''

    answer_text = 'Авторизуйтесь по ссылке:\n' + link
    chat_id = update.effective_chat.id

    # if this is a new user then add new structure, else update existing one
    if collection.find_one({'chat_id': chat_id}) is None:
        collection.insert_one(
            {
                "chat_id": update.effective_chat.id,
                "data": {
                    "twitter": {
                        "oauth_token": "",
                        "oauth_token_secret": "",
                        "last_seen_id": "",
                        "username": "",
                        "twi_statistics": {
                            "words": 0
                        },
                    },
                    "vk": {
                        "oauth_token": access_token,
                        "vk_statistics": {
                            "words": 0
                        },
                    },
                    "dvach": {
                        "dvach_statistics": {
                            "words": 0
                        }
                    },
                },
            }
        )
    else:
        collection.update_one({"chat_id": chat_id}, { "$set": {
            "data": {
                "vk": {
                    "oauth_token": access_token
                }
            }
        }})

    # session = vk_api.VkApi(token=ACCESS_TOKEN)
    # api = session.get_api()

    # Users = api.users.get()
    # print(Users[0]['first_name'])

    # this attempt to send user a message throws exceptions for some reason :\

    context.bot.send_message(
        chat_id=chat_id,
        text=answer_text
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

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Произошёл выход'
    )

    return VK_DEFAULT


def process_status(update, context):
    status_text = update.message.text
    answer_text = ''
    access_token = ''

    chat_id = update.effective_chat.id

    doc = collection.find_one({"chat_id": chat_id})
    if doc is not None:
        access_token = doc["data"]["vk"]["oauth_token"]

    try:
        answer_text = 'Вы поставили статус:\n' + status_text
        vk_api.VkApi(token=access_token).get_api().status.set(text=status_text)
    except vk_api.ApiError:
        answer_text = 'Ошибка аутентификации. Попробуйте перезайти'

    update.message.reply_text(
        answer_text,
        reply_markup=get_vk_markup()
    )

    return VK_DEFAULT


def process_post(update, context):
    post_text = update.message.text
    answer_text = ''
    access_token = ''

    chat_id = update.effective_chat.id

    doc = collection.find_one({"chat_id": chat_id})
    if doc is not None:
        access_token = doc["data"]["vk"]["oauth_token"]

    try:
        answer_text = 'Запощено'
        vk_api.VkApi(token=access_token).get_api().wall.post(message=post_text)
    except vk_api.ApiError:
        answer_text = 'Ошибка аутентификации. Попробуйте перезайти'

    update.message.reply_text(
        answer_text,
        reply_markup=get_vk_markup()
    )

    return VK_DEFAULT

