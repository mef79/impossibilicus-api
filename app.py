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
from util import Timeout

def main():
	app = Flask(__name__)

	# enable cross-origin requests
	CORS(app)

	# initialize the flask-api library
	api = Api(app)

	# initialize the mongo connection string variables
	uri = os.getenv('MONGODB_URI')
	username = os.getenv('MONGO_USERNAME')
	client = MongoClient(uri)

	# attempt to initialize story collection
	try:
		story_collection = client[username].story
	except TypeError:
		print ('Must enter Mongo username environment variable MONGO_USERNAME')
		print ('Failed to start')
		return

	try:
		with Timeout(3):
			client.admin.command('ismaster')
	except Timeout.Timeout:
		print ('Connection to MongoDB failed, check MONGODB_URI environment variable')
		print ('Failed to start')
		return

	dao = Dao(story_collection)

	api.add_resource(Home, '/')
	api.add_resource(Story, '/story', '/story/<string:name>',
		resource_class_kwargs={'dao':dao})
	api.add_resource(StoryList, '/stories',
		resource_class_kwargs={'dao':dao})
	api.add_resource(StoryImport, '/storyImport',
		resource_class_kwargs={'dao':dao})
	app.run()

if __name__ == '__main__':
	main()