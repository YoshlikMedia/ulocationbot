from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import CITIES
from data.texts import texts
from keyboards.default.keyboard import rating_keyboard
from keyboards.inline.cities_button import (branch_categories_button,
                                            categorie_button, cities_button)
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


@dp.callback_query_handler(lambda call: call.data == 'cancel', state=Form.GetCategory)
async def cancel_city_categories(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=_(texts['choose_city']), reply_markup=await cities_button())
    await state.finish()


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


@dp.callback_query_handler(lambda call: call.data == 'cancel', state=Form.GetInfo)
async def cancel_city_categories(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = City()
        print(data)
        await call.message.edit_text(
            text=_(texts['choose_categories']),
            reply_markup=await categorie_button(
                city.get_category_name(data['city'])
            )
        )
    await Form.GetCategory.set()


@dp.callback_query_handler(state=Form.GetInfo)
async def city_categories(call: types.CallbackQuery, state: FSMContext):
    city = City()
    async with state.proxy() as data:
        info = city.get_info_with_id(data['city'], call.data).get('info')
        data['_id'] = city.get_info_with_id(data['city'], call.data).get('_id')
        image = info.get('image')
        loc = info.get('location')
        rating = city.get_rating(data['city'], data['_id'])

        await call.message.answer_photo(image.get('image_url'), image.get('caption'))
        await call.message.answer_location(longitude=loc.get('longitude'), latitude=loc.get('latitude'))
        await call.message.answer(_(texts['rating_msg'].format(rating=rating)))
        await call.message.answer(_(texts['get_rating']), reply_markup=rating_keyboard)

        await Form.GetRating.set()


@dp.message_handler(state=Form.GetRating)
async def get_rating(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        city = City()
        city.add_rating(data['city'], data['_id'], len(msg.text) // 2)

    await msg.answer(_(texts['thanks_rate']))
