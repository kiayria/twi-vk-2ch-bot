from app import updater


if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
