from flask import jsonify
from errors import *

class Dao:
	def __init__(self, collection):
		self.collection = collection

	def save(self, data):
		exists = self.collection.find_one({"name":data['name']})
		if exists:
			raise AlreadyExistsError('Story with name \'' + data['name'] + '\' already exists')
		return self.collection.insert_one(data)

	def update(self, name, data):
		result = self.collection.update_one(
			{'name': name}, # query
			{ # update object
				'$set': {
					'name': data['name'],
					'nodes': data['nodes'],
					'links': data['links']
				}
			}
		)
		if result.matched_count < 1:
			raise UpdateError()

	def get_story(self, query):
		result = self.collection.find_one(query)
		if not result:
			raise NotFoundError('Story with name \'' + query['name'] + '\' not found')
		return result

	def get_all(self):
		stories = list(self.collection.find())
		for story in stories:
			story['_id'] = str(story['_id'])
		return jsonify(stories)