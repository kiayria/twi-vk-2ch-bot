from app.utils.keyboards import get_markup
from .buttons import TWITTER_BUTTONS, TWITTER_STREAM_BUTTONS


def get_twi_markup():
    return get_markup(TWITTER_BUTTONS)


def get_twi_stream_markup():
    return get_markup(TWITTER_STREAM_BUTTONS)
