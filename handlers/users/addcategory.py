from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.texts import texts
from loader import dp
from middlewares import i18n
from states.States import Form
from utils.db_api.database import Categories

_ = i18n.lazy_gettext


@dp.message_handler(Command('addcategory'))
async def add_category(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(_(texts['get_category_name']))
    await Form.GetCategoryName.set()


@dp.message_handler(state=Form.GetCategoryName)
async def get_category_name(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category_name'] = msg.text
    await msg.answer(_(texts['get_category_description']))
    await Form.GetCategoryDescription.set()


@dp.message_handler(state=Form.GetCategoryDescription)
async def get_category_description(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category_description'] = msg.text
        cat = Categories()
        cat.add_category(data['category_name'], data['category_description'])

    await msg.answer(_(texts['thanks_cat']))
    await state.finish()
