from app import db
from app.utils.states import CHOOSING
from app.utils.keyboards import get_start_markup


def start_menu(update, context):
    update.message.reply_text(
        text='Hi there! Let`s waste some time.',
        reply_markup=get_start_markup()
    )

    db.init_user(update.effective_chat.id)

    return CHOOSING


def back(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Hi there! Let`s waste some time.',
        reply_markup=get_start_markup()
    )

    return CHOOSING
