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
    VK_LOGIN,
    DVACH_DEFAULT,
    DVACH_POST,
    STATISTICS
)
from app.start_menu import start_menu, back
from app.twitter.commands import (
    twi_menu,
    twi_login,
    twi_tweet,
    twi_news,
    twi_stream,
    twi_stream_off,
    twi_logout,
    process_tweet,
    process_stream
)
from app.vk.commands import (
    vk_menu,
    vk_login,
    process_login_vk,
    vk_logout,
    vk_post,
    vk_change_status,
    process_status,
    process_post
)

from app.dvach.commands import (
    dvach_menu,
    dvach_post,
    dvach_news,
    process_dvach_post
)

from app.statistics.commands import (
    stat_menu,
    stat_all,
    stat_vk,
    stat_twitter,
    stat_2ch
)


def get_conversation():
    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start_menu)],
        states={
            CHOOSING: [
                CallbackQueryHandler(twi_menu, pattern='^twi_btn$'),
                CallbackQueryHandler(vk_menu, pattern='^vk_btn$'),
                CallbackQueryHandler(dvach_menu, pattern='^dvach_btn$'),
                CallbackQueryHandler(stat_menu, pattern='^stat_btn$'),
            ],
            TWITTER_DEFAULT: [
                CallbackQueryHandler(twi_login, pattern='^twi_login$'),
                CallbackQueryHandler(twi_tweet, pattern='^twi_tweet$'),
                CallbackQueryHandler(twi_news, pattern='^twi_news$'),
                CallbackQueryHandler(twi_stream, pattern='^twi_stream$'),
                CallbackQueryHandler(twi_logout, pattern='^twi_logout$'),
                CallbackQueryHandler(back, pattern='^return$'),
            ],
            TWITTER_TWEET: [
                MessageHandler(Filters.text, process_tweet),
                CallbackQueryHandler(back, pattern='^return$'),
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
                CallbackQueryHandler(back, pattern='^return$'),
            ],
            VK_LOGIN: [
                MessageHandler(Filters.text, process_login_vk),
                CallbackQueryHandler(back, pattern='^return$'),
            ],
            VK_POST: [
                MessageHandler(Filters.text, process_post),
                CallbackQueryHandler(back, pattern='^return$'),
            ],
            VK_STATUS: [
                MessageHandler(Filters.text, process_status),
                CallbackQueryHandler(back, pattern='^return$'),
            ],
            DVACH_DEFAULT: [
                CallbackQueryHandler(dvach_news, pattern='^dvach_news$'),
                CallbackQueryHandler(dvach_post, pattern='^dvach_post$'),
                CallbackQueryHandler(back, pattern='^return$'),
            ],
            DVACH_POST: [
                MessageHandler(Filters.text, process_dvach_post),
                CallbackQueryHandler(start_menu, pattern='^return$'),
            ],
            STATISTICS: [
                CallbackQueryHandler(stat_all, pattern='^stat_all$'),
                CallbackQueryHandler(stat_twitter, pattern='^stat_twitter$'),
                CallbackQueryHandler(stat_vk, pattern='^stat_vk$'),
                CallbackQueryHandler(stat_2ch, pattern='^stat_2ch$'),
                CallbackQueryHandler(back, pattern='^return$'),
            ]
        },
        fallbacks=[],
    )

    return conv
