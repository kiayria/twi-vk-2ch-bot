from api2ch.api import DvachApi
from api2ch.models import Message
from api2ch.captcha import CaptchaHelper
from api2ch.client import ApiClient

from app.dvach.utils.utils import stat_text
from app.dvach.utils.keyboards import DVACH_MARKUP, DVACH_POST_MARKUP
from app.utils.states import DVACH_DEFAULT, DVACH_POST


def dvach_menu(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Функции 2ch',
        reply_markup=DVACH_MARKUP
    )

    return DVACH_DEFAULT


def dvach_post(update, context):
    query = update.callback_query
    query.answer()

    _clear_dvach_user_data(context)
    query.edit_message_text(
        text='Введите текст сообщения',
        reply_markup=DVACH_POST_MARKUP
    )

    return DVACH_POST


def dvach_news(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text="Секундочку... Ищем смешные посты...",
        reply_markup=DVACH_MARKUP
    )

    api = DvachApi('b')

    # Top 10 threads sorted by posts count
    top = api.get_top(method='posts', num=10)

    txt = "Мы нашли эти посты:\n"
    for thread in top:
        txt += f"{thread.num} говорит:\n {thread.post.comment}\n * * * * * * * * *\n\n\n"

    context.bot.send_message(
        update.effective_chat.id,
        text=txt,
        reply_markup=DVACH_MARKUP
    )

    return DVACH_DEFAULT    


def _clear_dvach_user_data(context):
    context.user_data.pop('dvach_post', None)
    context.user_data.pop('dvach_board', None)
    context.user_data.pop('dvach_thread_id', None)
    context.user_data.pop('dvach_capcha_helper', None)



def process_dvach_post(update, context):
    state = DVACH_POST

    if 'dvach_post' not in context.user_data:
        text = update.message.text
        context.user_data['dvach_post'] = text
        answer_text = 'Введите название доски'

    elif 'dvach_board' not in context.user_data:
        text = update.message.text
        if DvachApi().board_exist(text):
            context.user_data['dvach_board'] = text
            answer_text = 'Введите номер треда'
        else:
            answer_text = 'Такой доски не существует! Введите название доски'

    elif 'dvach_thread_id' not in context.user_data:
        text = update.message.text
        try:
            context.user_data['dvach_thread_id'] = int(text)
        except:
            answer_text = f'Это не число!'
            update.message.reply_text(
                answer_text,
                reply_markup=DVACH_POST_MARKUP
            )
            return state


        api_session = ApiClient()

        helper = CaptchaHelper(api_session.session)
        captcha = helper.get_captcha()
        context.user_data['dvach_capcha_helper'] = helper
        context.user_data['dvach_capcha'] = captcha
        captcha_url = helper.get_captcha_img(captcha).url

        answer_text = f'Пройдите капчу: {captcha_url}' 

    elif 'dvach_capcha_helper' in context.user_data and 'dvach_capcha' in context.user_data:
        text = update.message.text

        helper = context.user_data['dvach_capcha_helper']
        captcha = context.user_data['dvach_capcha']
        captcha.set_answer(text)

        if helper.check_captcha(captcha):
            board = context.user_data['dvach_board']
            thread_id = context.user_data['dvach_thread_id']
            dvach_post = context.user_data['dvach_post']

            api = DvachApi(board=board)
            message = Message(board_id=api.board.id, thread_id=thread_id, comment=dvach_post, sage=True)
            api.send_post(message=message, captcha=captcha)
            stat_text(update.effective_chat.id, dvach_post)
            answer_text = 'Пост отправлен!'
            _clear_dvach_user_data(context)
            state = DVACH_DEFAULT
        else:
            answer_text = 'Капча введена неправильно! Пост не отправлен'
            _clear_dvach_user_data(context)
            state = DVACH_DEFAULT
    else:
        answer_text = 'Произошло что-то непонятное! Попробуйте снова.'    
        _clear_dvach_user_data(context)
        state = DVACH_DEFAULT

    update.message.reply_text(
        answer_text,
        reply_markup=DVACH_POST_MARKUP
    )
    return state
