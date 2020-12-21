from app.utils.states import CHOOSING
from app.utils.keyboards import get_start_markup


def start_menu(update, context):
    update.message.reply_text(
        text='Hi there! Let`s waste some time.',
        reply_markup=get_start_markup()
    )

    return CHOOSING
