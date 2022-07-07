from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import CITIES
from middlewares import i18n
from utils.db_api.mongo import CATEGORIES

_ = i18n.lazy_gettext


async def cities_button(cites=CITIES):
    markup = InlineKeyboardMarkup(row_width=2)
    for city in cites:
        markup.add(InlineKeyboardButton(text=_(cites[city]), callback_data=city))
    return markup


async def categorie_button(categories):
    markup = InlineKeyboardMarkup()
    for category in set(categories):
        markup.add(InlineKeyboardButton(text=CATEGORIES.find_one().get(category), callback_data=category))
    return markup


async def branch_categories_button(categories):
    markup = InlineKeyboardMarkup()
    for category in categories:
        _id, name = category['_id'], category['info']['address']
        markup.add(InlineKeyboardButton(text=name, callback_data=str(_id)))
    return markup
