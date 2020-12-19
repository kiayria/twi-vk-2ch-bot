from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.utils.buttons import (
    START_BUTTONS,
    TWITTER_BUTTONS, VK_BUTTONS
)


def get_start_markup():
    start_kb = InlineKeyboardMarkup(row_width=2)
    for line in START_BUTTONS:
        buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in line)
        start_kb.row(*buttons)

    return start_kb


def get_hidden_markup():
    hidden_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            'Развернуть',
            callback_data='expand'
        )
    )

    return hidden_kb


def get_twi_markup():
    twi_kb = InlineKeyboardMarkup(row_width=2)
    for line in TWITTER_BUTTONS:
        buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in line)
        twi_kb.row(*buttons)

    return twi_kb


def get_vk_markup():
    vk_kb = InlineKeyboardMarkup(row_width=2)
    for line in VK_BUTTONS:
        buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in line)
        vk_kb.row(*buttons)

    return vk_kb
