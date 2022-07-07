from pymongo import MongoClient
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from data.config import IP

client = MongoClient(IP)
storage = MongoStorage()

database = client['ulocationbot']

LANG_STORAGE = database['lang_storage']
USERS = database['users']
CITY = database['city']
CATEGORIES = database['categories']