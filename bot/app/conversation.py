from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters
)
from app.utils.states import (
    CHOOSING,
    TWITTER_DEFAULT,
    TWITTER_TWEET,
    TWITTER_STREAM,
    VK_DEFAULT,
    VK_POST,
    VK_STATUS,
    DVACH
)
from app.start_menu import start_menu
from app.twitter.commands import (
    twi_menu,
    twi_login,
    twi_tweet,
    twi_news,
    twi_stream,
    twi_stream_off,
    process_tweet,
    process_stream
)
from app.vk.commands import (
    vk_menu,
    vk_login,
    vk_logout,
    vk_post,
    vk_change_status,
    process_status,
    process_post
)


def get_conversation():
    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start_menu)],
        states={
            CHOOSING: [
                CallbackQueryHandler(twi_menu, pattern='^twi_btn$'),
                CallbackQueryHandler(vk_menu, pattern='^vk_btn$'),
            ],
            TWITTER_DEFAULT: [
                CallbackQueryHandler(twi_login, pattern='^twi_login$'),
                CallbackQueryHandler(twi_tweet, pattern='^twi_tweet$'),
                CallbackQueryHandler(twi_news, pattern='^twi_news$'),
                CallbackQueryHandler(twi_stream, pattern='^twi_stream$'),
            ],
            TWITTER_TWEET: [
                MessageHandler(Filters.text, process_tweet)
            ],
            TWITTER_STREAM: [
                MessageHandler(Filters.text, process_stream),
                CallbackQueryHandler(twi_stream_off, pattern='^twi_stream_off$'),
            ],
            VK_DEFAULT: [
                CallbackQueryHandler(vk_login, pattern='^vk_login$'),
                CallbackQueryHandler(vk_post, pattern='^vk_post$'),
                CallbackQueryHandler(vk_change_status, pattern='^vk_change_status$'),
                CallbackQueryHandler(vk_logout, pattern='^vk_logout$'),
            ],
            VK_POST: [
                MessageHandler(Filters.text, process_post)
            ],
            VK_STATUS: [
                MessageHandler(Filters.text, process_status)
            ],
            DVACH: []
        },
        fallbacks=[],
    )

    return conv
