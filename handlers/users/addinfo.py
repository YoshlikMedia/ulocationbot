import json

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import CITIES
from data.texts import texts
from keyboards.default.keyboard import rating_keyboard
from keyboards.inline.cities_button import categorie_button, cities_button, branch_categories_button
from loader import dp
from middlewares import i18n
from states.States import Form
from utils.db_api.database import City

_ = i18n.lazy_gettext


@dp.message_handler(Command('addinfo'), state='*')
async def add_info(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(text=_(texts['choose_city']), reply_markup=await cities_button())
    await state.finish()
    await Form.GetCategoryAdd.set()


@dp.callback_query_handler(lambda call: call.data in CITIES.keys(), state=Form.GetCategoryAdd)
async def city_categories(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        city = City()
        await call.message.edit_text(
            text=_(texts['choose_categories']),
            reply_markup=await categorie_button()
        )
        await Form.GetCategoryAddInfo.set()
        data['city'] = call.data


@dp.callback_query_handler(state=Form.GetCategoryAddInfo)
async def city_categories(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = call.data
    await call.message.edit_text(_(texts['get_caption']))
    await Form.GetCaption.set()


@dp.message_handler(state=Form.GetCaption)
async def get_caption(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['caption'] = msg.text
    await msg.answer(_(texts['get_image']))
    await Form.GetImage.set()


@dp.message_handler(state=Form.GetImage, content_types=types.ContentType.PHOTO)
async def get_image(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['image'] = msg.photo[0].file_id
    await msg.answer(_(texts['get_info']))
    await Form.GetInfoAdd.set()


@dp.message_handler(state=Form.GetInfoAdd)
async def get_info(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info'] = msg.text
    await msg.answer(_(texts['get_location']))
    await Form.GetLocation.set()


@dp.message_handler(state=Form.GetLocation, content_types=types.ContentType.LOCATION)
async def get_location(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = dict(msg.location)
    await msg.answer(_(texts['get_rating']), reply_markup=rating_keyboard)
    await Form.GetRatingAdd.set()


@dp.message_handler(state=Form.GetRatingAdd)
async def get_rating(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['rating'] = len(msg.text) // 2
        print(data)
        city = City()
        city.adding_base_info(
            data['city'],
            data['category'],
            {
                'address': data['caption'],
                'image': {
                    "image_url": data['image'],
                    "caption": data['info']
                },
                "location": {
                    "latitude": data.get('location').get('latitude'),
                    "longitude": data.get('location').get('longitude')
                },
                "rating": data['rating'],
            }
        )

    await msg.answer(_(texts['thanks_msg']))

    await state.finish()
