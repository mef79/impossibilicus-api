from flask import jsonify, request
from flask_restful import Resource
from errors import *
from util import *

class Home(Resource):
	def get(self):
		return {'status': 'ok'}

class Story(Resource):
	def __init__(self, **kwargs):
		self.dao = kwargs['dao']

	def post(self):
		try:
			print(request.get_json())
			data = validate(request.get_json())
			result = self.dao.save(data)
			return str(result.inserted_id)

		except AssertionError:
			return error('Invalid input'), 400

		except AlreadyExistsError as e:
			return error(str(e)), 400

	def get(self, name):
		try:
			result = self.dao.get_story({"name":name})
			result['_id'] = str(result['_id']) # ObjectId is not serializable
			return jsonify(result)

		except NotFoundError as e:
			return error(str(e)), 404

	def put(self, name):
		try:
			self.dao.get_story({'name':name}) # make sure the story exists
			data = validate(request.get_json())
			return self.dao.update(name, data)

		except AssertionError:
			return error('Invalid input'), 400

		except NotFoundError as e:
			return error(str(e)), 404

		except UpdateError:
			return error('Update failed'), 500

class StoryList(Resource):
	def __init__(self, **kwargs):
		self.dao = kwargs['dao']

	def get(self):
		return self.dao.get_all()