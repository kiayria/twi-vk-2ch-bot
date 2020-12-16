from aiogram.dispatcher.filters.state import State, StatesGroup


class TwitterForm(StatesGroup):
    tweet = State()
    stream = State()
    news = State()


class Form(StatesGroup):
    twitter = State()
    vk = State()
    dvach = State()
