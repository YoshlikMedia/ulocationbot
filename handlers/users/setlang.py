from aiogram import types

from data.config import LANGUAGES, LANG_STORAGE
from loader import dp


@dp.callback_query_handler(lambda c: c.data in LANGUAGES)
async def set_lang(call: types.CallbackQuery):
    print(call.data)
    LANG_STORAGE[call.from_user.id] = call.data
    await call.message.edit_text(text=f"Вы выбрали язык {call.data}")