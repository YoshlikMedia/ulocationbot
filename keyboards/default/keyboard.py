from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.texts import texts
from middlewares import i18n

_ = i18n.lazy_gettext

get_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text=_(texts['get_phone_number']),
                request_contact=True
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

rating_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("⭐️⭐️⭐️"),
            KeyboardButton("⭐️⭐️"),
            KeyboardButton("⭐️")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
