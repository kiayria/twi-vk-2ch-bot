from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .buttons import START_BUTTONS


def get_markup(buttons):
    keyboard = [[InlineKeyboardButton(text, callback_data=data) for text, data in line] for line in buttons]
    kb = InlineKeyboardMarkup(keyboard)

    return kb


def get_start_markup():
    return get_markup(START_BUTTONS)
