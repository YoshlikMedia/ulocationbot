from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    # Get information states
    GetName = State()
    GetPhone = State()

    # Categories states
    GetCategory = State()
    GetInfo = State()
    GetRating = State()

    # Adding Information states
    GetCategoryAdd = State()
    GetCategoryAddInfo = State()
    GetCaption = State()
    GetImage = State()
    GetInfoAdd = State()
    GetLocation = State()
    GetRatingAdd = State()

    # Adding new category states
    GetCategoryName = State()
    GetCategoryDescription = State()
