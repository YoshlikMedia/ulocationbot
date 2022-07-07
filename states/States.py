from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    # Get information states
    GetName = State()
    GetPhone = State()

    # Categories states
    GetCategory = State()
    GetInfo = State()