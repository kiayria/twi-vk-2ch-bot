from app.statistics.utils.utils import get_stat
from app.statistics.utils.keyboards import STATISTICS_MARKUP
from app.utils.states import STATISTICS


def stat_menu(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Доступная статистика',
        reply_markup=STATISTICS_MARKUP
    )

    return STATISTICS


def stat_all(update, context):
    query = update.callback_query
    query.answer()

    words = get_stat(update.effective_chat.id)
    print(words)
    if words is None:
        query.edit_message_text(
            text='Нет выбранной статистики для этого чата.',
            reply_markup=STATISTICS_MARKUP
        )
    else:
        text = '\n'.join([f'{k}: {v}' for k, v in words.items()])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )

    return STATISTICS


def stat_twitter(update, context):
    query = update.callback_query
    query.answer()

    words = get_stat(update.effective_chat.id, 'twitter')
    if words is None:
        query.edit_message_text(
            text='Нет выбранной статистики для этого чата.',
            reply_markup=STATISTICS_MARKUP
        )
    else:
        text = '\n'.join([f'{k}: {v}' for k, v in words.items()])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )

    return STATISTICS


def stat_vk(update, context):
    query = update.callback_query
    query.answer()

    words = get_stat(update.effective_chat.id, 'vk')
    if words is None:
        query.edit_message_text(
            text='Нет выбранной статистики для этого чата.',
            reply_markup=STATISTICS_MARKUP
        )
    else:
        text = '\n'.join([f'{k}: {v}' for k, v in words.items()])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )

    return STATISTICS


def stat_2ch(update, context):
    query = update.callback_query
    query.answer()

    words = get_stat(update.effective_chat.id, 'dvach')
    if words is None:
        query.edit_message_text(
            text='Нет выбранной статистики для этого чата.',
            reply_markup=STATISTICS_MARKUP
        )
    else:

        text = '\n'.join([f'{k}: {v}' for k, v in words.items()])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
        )

    return STATISTICS
