from aiogram import types

from data.config import LANGUAGES
from data.texts import texts
from loader import dp
from middlewares import i18n
from utils.db_api.mongo import LANG_STORAGE

_ = i18n.lazy_gettext


@dp.callback_query_handler(lambda c: c.data in LANGUAGES)
async def set_lang(call: types.CallbackQuery):
    LANG_STORAGE.update_one({"user_id": call.from_user.id}, {"$set": {"lang": call.data}})
    await call.message.edit_text(_(texts['choose_city'], locale=call.data))
