from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choose_lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="O'zbek",
                callback_data="uz"
            ),
            InlineKeyboardButton(
                text="Русский",
                callback_data="ru"
            )
        ]
    ]
)
