import os
import sys
from flask import Flask
from pymongo import MongoClient
from flask_restful import Api
from dao import Dao
from resources import *
from flask_cors import CORS

# imports from other files
from errors import NotFoundError, UpdateError
from resources import Home, Story, StoryList

app = Flask(__name__)
CORS(app)
api = Api(app)
uri = os.getenv('MONGODB_URI')
username = os.getenv('MONGO_USERNAME')
client = MongoClient(uri)
story_collection = client[username].story
dao = Dao(story_collection)

api.add_resource(Home, '/')
api.add_resource(Story, '/story', '/story/<string:name>',
	resource_class_kwargs={'dao':dao})
api.add_resource(StoryList, '/stories',
	resource_class_kwargs={'dao':dao})

if __name__ == '__main__':
	app.run()