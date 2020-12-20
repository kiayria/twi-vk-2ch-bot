from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.buttons import (
    START_BUTTONS,
    TWITTER_BUTTONS, VK_BUTTONS
)


def get_start_markup():
    keyboard = [[InlineKeyboardButton(text, callback_data=data) for text, data in line] for line in START_BUTTONS]
    start_kb = InlineKeyboardMarkup(keyboard)

    return start_kb


# def get_hidden_markup():
#     hidden_kb = InlineKeyboardMarkup().add(
#         InlineKeyboardButton(
#             'Развернуть',
#             callback_data='expand'
#         )
#     )
#
#     return hidden_kb


def get_twi_markup():
    keyboard = [[InlineKeyboardButton(text, callback_data=data) for text, data in line] for line in TWITTER_BUTTONS]
    twi_kb = InlineKeyboardMarkup(keyboard)

    return twi_kb


def get_vk_markup():
    keyboard = [[InlineKeyboardButton(text, callback_data=data) for text, data in line] for line in VK_BUTTONS]
    vk_kb = InlineKeyboardMarkup(keyboard)

    return vk_kb
