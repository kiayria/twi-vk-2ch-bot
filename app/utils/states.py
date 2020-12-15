from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    twitter = State()
    vk = State()
    dvach = State()
