from aiogram import types

from loader import dp


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def location_handler(message: types.Message):
    loc = dict(message.location)
    print(loc.get('latitude'))
    print(type(loc))
    print(loc)
    print(message.location.as_json())
    await message.answer_location(message.location.latitude, message.location.longitude)


@dp.callback_query_handler()
async def callback_query_handler(callback_query: types.CallbackQuery):
    print(callback_query.data)
