from app.utils.keyboards import get_markup
from .buttons import DVACH_DEFAULT_BUTTONS, DVACH_POST_BUTTONS


def get_dvach_markup():
    return get_markup(DVACH_DEFAULT_BUTTONS)

def get_dvach_post_markup():
    return get_markup(DVACH_POST_BUTTONS)