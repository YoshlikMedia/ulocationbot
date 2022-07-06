from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    GetName = State()
    GetPhone = State()
