from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.texts import texts
from keyboards.inline.lang_keyboard import choose_lang
from loader import dp

# Alias for gettext method
from middlewares import i18n

_ = i18n.lazy_gettext


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer(text=texts['welcome'])
    await message.answer(text=texts['change_language'], reply_markup=choose_lang)