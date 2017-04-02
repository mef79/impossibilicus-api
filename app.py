import os
import sys
import sqlite3
from flask import Flask, request, jsonify, abort, Response
from pymongo import MongoClient

app = Flask(__name__)
uri = os.getenv('MONGODB_URI')
username = os.getenv('MONGO_USERNAME')
password = os.getenv('MONGO_PASSWORD')
client = MongoClient(uri)
story_collection = client[username].story

@app.route('/')
def confirm_running():
	return 'The app is running'

@app.route('/story', methods=['POST'])
def story():
	return save(request)

@app.route('/story/<name>', methods=['GET', 'PUT'])
def get_story(name):
	print story
	sys.stdout.flush()
	result = story_collection.find_one({"name":name})
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

	result = story_collection.insert_one(data)
	return str(result.inserted_id)

def update(name, request):
	data = request.get_json()
	if not validate(data):
		return response('Invalid input', 400)

	result = story.update_one(
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
	app.run()