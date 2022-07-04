from aiogram import types

from middlewares import i18n

_ = i18n.lazy_gettext


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", _("Botni ishga tushirish")),
            types.BotCommand("help", _("Yordam")),
            types.BotCommand("settings", _("Sozlamalar")),
            types.BotCommand("lang", _("Til")),
            types.BotCommand("city", _("Shahar")),
            types.BotCommand("place", _("Joylar")),
            types.BotCommand("about", _("Bot haqida")),
        ]
    )
