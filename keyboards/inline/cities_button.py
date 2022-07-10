from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import CITIES
from middlewares import i18n
from utils.db_api.database import Categories
from utils.db_api.mongo import CATEGORIES

_ = i18n.lazy_gettext


async def cities_button(cites=CITIES):
    button = []
    for city in cites:
        button.append(InlineKeyboardButton(text=_(cites[city]), callback_data=city))
    return InlineKeyboardMarkup(inline_keyboard=[button])


async def categorie_button(categories=None):
    markup = InlineKeyboardMarkup()
    if categories is None:
        cat = Categories()
        categories = cat.get_all_categories()

        for category in categories:
            getName = category.get('category_name')
            getInfo = category.get('category_info')
            markup.add(InlineKeyboardButton(text=getInfo, callback_data=getName))
        return markup

    for category in set(categories):
        getInfo = CATEGORIES.find_one({'category_name': category}).get('category_info')
        markup.add(InlineKeyboardButton(text=getInfo, callback_data=category))
    return markup


async def branch_categories_button(categories):
    markup = InlineKeyboardMarkup()
    for category in categories:
        _id, name = category['_id'], category['info']['address']
        markup.add(InlineKeyboardButton(text=name, callback_data=str(_id)))
    return markup
