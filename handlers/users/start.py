from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.texts import texts
from keyboards.default.keyboard import get_number
from keyboards.inline.cities_button import cities_button
from keyboards.inline.lang_keyboard import choose_lang
from loader import dp
from middlewares import i18n
from states.States import Form
from utils.db_api.mongo import USERS

_ = i18n.lazy_gettext


@dp.message_handler(CommandStart(), state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text=texts['welcome'])

    if USERS.find_one({'user_id': message.from_user.id}) is None:
        await message.answer(text=texts['change_language'], reply_markup=choose_lang)
        return

    if not USERS.find_one({'user_id': message.from_user.id}).get('name', False):
        await message.answer(text=_(texts['get_full_name']))
        await Form.GetName.set()
        return

    if not USERS.find_one({'user_id': message.from_user.id}).get('phone', False):
        await message.answer(text=_(texts['get_phone_number']), reply_markup=get_number)
        await Form.GetPhone.set()
        return

    await message.answer(text=_(texts['choose_city']), reply_markup=await cities_button())


@dp.message_handler(state=Form.GetName)
async def get_name(message: types.Message, state: FSMContext):
    USERS.update_one({'user_id': message.from_user.id}, {'$set': {'name': message.text}})
    if not USERS.find_one({'user_id': message.from_user.id}).get('phone', False):
        await message.answer(text=texts['get_phone_number'], reply_markup=get_number)
        await Form.GetPhone.set()
        return

    await state.finish()
    await message.answer(text=_(texts['choose_city']), reply_markup=await cities_button())


@dp.message_handler(state=Form.GetPhone, content_types=types.ContentType.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    USERS.update_one({'user_id': message.from_user.id}, {'$set': {'phone': message.contact.phone_number}})
    await state.finish()

    await message.answer(text=_(texts['choose_city']), reply_markup=await cities_button())
