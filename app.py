import os
import sqlite3
from flask import Flask, request, jsonify, abort, Response
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def confirm_running():
	return 'The app is running'

@app.route('/story', methods=['POST'])
def story():
	return save(request)

@app.route('/story/<name>', methods=['GET', 'PUT'])
def get_story(name):
	result = mongo.db.story.find_one({"name":name})
	if result:
		if request.method == 'GET':
			result['_id'] = str(result['_id']) # ObjectId is not serializable
			return jsonify(result)
		else:
			return update(name, request)

	else: # query returned no results
		return resonse('Not found', 404)

def save(request):
	data = request.get_json()

	# 400 if the request
	if not validate(data):
		return response('Invalid input', 400)

	result = mongo.db.story.insert_one(data)
	return str(result.inserted_id)

def update(name, request):
	data = request.get_json()
	if not validate(data):
		return response('Invalid input', 400)

	result = mongo.db.story.update_one(
		{'name': name},
		{
			'$set': {
				'name': data['name'],
				'nodes': data['nodes'],
				'links': data['links']
			}
		}
	)
	if result.matched_count > 0:
		return response('OK', 200)
	return response('Update failed', 500)

def validate(data):
	return 'name' in data and 'nodes' in data and 'links' in data

def response(message, code):
	response = Response(message)
	response.status_code = code
	return response

if __name__ == '__main__':
	env_config = {
		'MONGO_URI': os.getenv('MONGODB_URI')
	}
	with open('config.cfg', 'w') as config_file:
		for key in env_config:
			config_file.write(key + '="' + env_config[key] + '"')
	app.config.from_pyfile('config.cfg')
	print app.config
	app.run()