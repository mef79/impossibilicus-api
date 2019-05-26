from flask import jsonify
from errors import *
import textract
from werkzeug import secure_filename, FileStorage
import os
from link import Link
from node import Node
import pprint

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

	def import_story(self, title, file):
		# get sanitized file name
		name = secure_filename(file.filename)

		pp = pprint.PrettyPrinter(indent=4)

		# save the file in the temp directory so it can be processed
		target = os.path.join('/tmp/', name)
		file.save(target)
		extracted = textract.process(target).decode(encoding='UTF-8')

		# all the lines of the file
		lines = [line for line in extracted.split('\n')]

		# strip whitespace and empty lines
		clean_lines = [line.rstrip() for line in lines if len(line.rstrip()) > 0]
		pp.pprint(clean_lines)
		node_counter = 0
		link_counter = 0
		nodes = []
		links = []
		current_type = 'node'

		# links that are waiting for the next node
		links_to_link = []

		# links that are waiting for the next non-indented node
		childless_links = []

		for line in clean_lines:
			# if this has no bullet/indent, it is a node
			if line[0] is not '*' and line[0] is not ' ':
				current_type = 'node'
				indent_level = 0

			# one indent: link
			elif line[0] is '*':
				current_type = 'link'
				indent_level = 1
				line = line[1:]

			# two indents: node
			elif line[0:4] == '   *':
				current_type = 'node'
				indent_level = 2
				line = line[5:]

			# three indents: link
			# TODO: refactor
			elif line[0:7] == '      *':
				current_type = 'link'
				indent_level = 3
				line = line[8:]

			if current_type == 'node':
				node = Node(**{
					'id': 'node-' + str(node_counter),
					'text': line,
					'indent_level': indent_level
				})
				node_counter += 1
				nodes.append(node)

				# check all links that are waiting for their target
				for link in links_to_link:
					# if this node is more indented, then this node is their target
					if link.indent_level == node.indent_level - 1:
						link.target = node
						links.append(link)
					# otherwise this link's target is the next non-indented node
					else:
						childless_links.append(link)

				# waiting links have been linked to this node or marked childless
				links_to_link = []

				# non-indented: set as the child for any childless links
				# TODO: distinguishing between {next} and {next timestamp}
				if indent_level == 0:
					for link in childless_links:
						link.target = node
						links.append(link)
					childless_links = []

			else:
				# the source is the last node in the list at one lower indent
				for node in nodes[::-1]:
					if node.indent_level == indent_level - 1:
						source_node = node
						break

				link = Link(**{
					'id': 'link-' + str(link_counter),
					'text': line,
					'source': source_node,
					'indent_level': indent_level
				})

				links_to_link.append(link)

				link_counter += 1

		story = {
			'name': title,
			'nodes': [dict(node) for node in nodes],
			'links': [dict(link) for link in links]
		}
		self.save(story)
		return self.get_story({"name":title})