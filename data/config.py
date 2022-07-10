from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

I18N_DOMAIN = 'ulocationbot'

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

LANGUAGES = ['uz', 'ru']

CITIES = {
    "bukhara": "Buxoro",
    "tashkent": "Tashkent",
    "samarkand": "Samarkand"
}
