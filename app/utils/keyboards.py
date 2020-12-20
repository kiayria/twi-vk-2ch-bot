from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.utils.buttons import (
    START_BUTTONS,
    TWITTER_BUTTONS,
    TWITTER_STREAM_BUTTONS,
    VK_BUTTONS
)


def get_markup(buttons):
    keyboard = [[InlineKeyboardButton(text, callback_data=data) for text, data in line] for line in buttons]
    kb = InlineKeyboardMarkup(keyboard)

    return kb


def get_start_markup():
    return get_markup(START_BUTTONS)


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
    return get_markup(TWITTER_BUTTONS)


def get_twi_stream_markup():
    return get_markup(TWITTER_STREAM_BUTTONS)


def get_vk_markup():
    return get_markup(VK_BUTTONS)
