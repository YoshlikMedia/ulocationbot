from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import CITIES
from data.texts import texts
from keyboards.inline.cities_button import categorie_button, branch_categories_button
from loader import dp
from middlewares import i18n
from states.States import Form
from utils.db_api.database import City

_ = i18n.lazy_gettext


@dp.callback_query_handler(lambda call: call.data in CITIES.keys())
async def city_categories(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = City()
        await call.message.edit_text(
            text=_(texts['choose_categories']),
            reply_markup=await categorie_button(
                city.get_category_name(call.data)
            )
        )
        await Form.GetCategory.set()
        data['city'] = call.data


@dp.callback_query_handler(state=Form.GetCategory)
async def city_categories(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = City()
        await call.message.edit_text(
            text=_(texts['choose_category'].format(category=call.data)),
            reply_markup=await branch_categories_button(
                city.get_category_info(data['city'], call.data)
            ),
        )
    await Form.GetInfo.set()


@dp.callback_query_handler(state=Form.GetInfo)
async def city_categories(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = City()
        info = city.get_info_with_id(data['city'], call.data).get('info')
        await call.message.edit_text(
            "<code>{}</code>".format(info),
        )