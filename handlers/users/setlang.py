from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import LANGUAGES
from data.texts import texts
from keyboards.default.keyboard import get_number
from keyboards.inline.cities_button import cities_button
from keyboards.inline.lang_keyboard import choose_lang
from loader import dp
from middlewares import i18n
from states.States import Form
from utils.db_api.mongo import LANG_STORAGE, USERS

_ = i18n.lazy_gettext


@dp.message_handler(Command('lang'), state="*")
async def cmd_lang(message: types.Message):
    await message.answer(text=texts['change_language'], reply_markup=choose_lang)


@dp.callback_query_handler(lambda c: c.data in LANGUAGES)
async def set_lang(call: types.CallbackQuery):
    LANG_STORAGE.update_one({"user_id": call.from_user.id}, {"$set": {"lang": call.data}}, upsert=True)
    USERS.update_one({"user_id": call.from_user.id}, {"$set": {"lang": call.data}}, upsert=True)

    if not USERS.find_one({'user_id': call.from_user.id}).get('name', False):
        await call.message.answer(text=_(texts['get_full_name']))
        await Form.GetName.set()
        return

    if not USERS.find_one({'user_id': call.from_user.id}).get('phone', False):
        await call.message.answer(text=_(texts['get_phone_number']), reply_markup=get_number)
        await Form.GetPhone.set()
        return

    await call.message.edit_text(text=_(texts['choose_city'], locale=call.data), reply_markup=await cities_button())
