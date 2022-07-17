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
    await msg.answer(_(texts['get_info_uz']))
    await Form.GetInfoUz.set()


@dp.message_handler(state=Form.GetInfoUz)
async def get_info(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_uz'] = msg.text
    await msg.answer(_(texts['get_info_ru']))
    await Form.GetInfoRu.set()


@dp.message_handler(state=Form.GetInfoRu)
async def get_info(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_ru'] = msg.text
    await msg.answer(_(texts['get_location']))
    await Form.GetLocation.set()


@dp.message_handler(state=Form.GetLocation, content_types=[types.ContentType.LOCATION, types.ContentType.VENUE])
async def get_location(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        city = City()
        data['location'] = dict(msg.location)
        city.adding_base_info(
            data['city'],
            data['category'],
            {
                'address': data['caption'],
                'image': {
                    "image_url": data['image'],
                    "caption": {
                        "uz": data['info_uz'],
                        "ru": data['info_ru']
                    }
                },
                "location": {
                    "latitude": data.get('location').get('latitude'),
                    "longitude": data.get('location').get('longitude')
                },
                "rating": 0,
            }
        )

    await msg.answer(_(texts['thanks_msg']))

    await state.finish()
