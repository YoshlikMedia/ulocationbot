from typing import Dict, List

from bson import ObjectId

from utils.db_api.mongo import database
from pydantic import BaseModel


class ImagePost(BaseModel):
    image_url: List[str]
    caption: str = None


class Reserve(BaseModel):
    caption: str
    link: str


class Location(BaseModel):
    longitude: float
    latitude: float


class CityCategories(BaseModel):
    address: str
    image: ImagePost
    description: str
    reserve: Reserve = None
    location: Location = None
    taxi: str = None
    order: str = None
    rating: int = 0


class City:
    def create_city_collection(self, city_name):
        """
        Create collection in mongoDB
        """
        return database[city_name]

    def adding_base_info(self, city_name, category, info):
        """
        Add base info to collection
        """
        city_collection = self.create_city_collection(city_name)
        city_collection.insert_one({
            'category': category,
            'info': info
        })

    def get_category_name(self, city_name):
        """
        Get all categories from collection
        """
        for category in database[city_name].find():
            yield category['category']

    def get_category_info(self, city_name, category):
        """
        Get info from collection
        """
        for info in database[city_name].find({'category': category}):
            yield info

    def get_info_with_id(self, city_name, _id: str):
        """
        Get info from collection
        """
        return database[city_name].find_one({'_id': ObjectId(_id)})


class Categories:
    def add_category(self, category_name, category_info):
        """
        Add category to collection
        """
        category_collection = database.categories
        category_collection.update_one({
            category_name: category_info
        }, {
            '$set': {
                category_name: category_info
            }
        }, upsert=True)

    def get_category(self, category_name):
        """
        Get category from collection
        """
        category_collection = database.categories
        for category in category_collection.find():
            if category_name in category:
                return category[category_name]

    def get_all_categories(self):
        """
        Get all categories from collection
        """
        category_collection = database.categories
        for category in category_collection.find():
            yield category


if __name__ == "__main__":
    city1 = City()
    category1 = Categories()

    category1.add_category('cafe', 'Coffe ☕️')

    city1.adding_base_info('bukhara', 'cafe', {
        'address': 'Black Bear Coffee',
        'image': {
            'image_url': [
                'https://images.unsplash.com/photo-1518791841217-8f162f1e1131?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=800&q=60'],
            'caption': 'Cafe'
        },
        'info': 'Cafe in Tashkent',
    })
