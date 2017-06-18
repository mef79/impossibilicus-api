from flask import jsonify
from errors import *
import textract
from werkzeug import secure_filename, FileStorage
import pprint
import os
from link import Link
from node import Node

class Dao:
	def __init__(self, collection):
		self.collection = collection

	def save(self, data):
		exists = self.collection.find_one({"name":data['name']})
		print ('exists: ')
		print (exists)
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

	def import_story(self, file):
		name = secure_filename(file.filename)
		print (name)
		target = os.path.join('/tmp/', name)
		file.save(target)
		extracted = textract.process(target).decode(encoding='UTF-8')
		lines = [line for line in extracted.split('\n') if len(line) > 0]
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(lines)

		node_counter = 0
		link_counter = 0
		nodes = []
		links = []
		current_type = 'node'
		links_to_link = []
		childless_links = []

		for line in lines:
			# if this has no bullet/indent, it is actually a node
			if line[0] is not '*' and line[0] is not ' ':
				current_type = 'node'
				indentation_level = 0

			# one indent - is link
			elif line[0] is '*':
				current_type = 'link'
				indentation_level = 1
				line = line[1:]

			elif line[0:4] == '   *':
				current_type = 'node'
				indentation_level = 2
				line = line[5:]

			elif line[0:7] == '      *':
				current_type = 'link'
				indentation_level = 3
				line = line[8:]

			if current_type == 'node':
				print ('adding node for: "' + line[:40] + '..."')
				node = Node(**{
					'id': 'node-' + str(node_counter),
					'text': line,
					'indentation_level': indentation_level
				})
				node_counter += 1
				nodes.append(node)

				print ('links that are currently waiting:')
				pp.pprint(links_to_link)
				# check all links that are waiting for their target
				for link in links_to_link:
					# if this node is more indented, then this node is their target
					if link.indentation_level == node.indentation_level - 1:
						print ('this node is the target for (' + link.text + ')')
						link.target = node
						links.append(link)
					# otherwise this link's target is the next non-indented node
					else:
						childless_links.append(link)
				links_to_link = []

				# if this is a non-indented node, it's the target for links that didn't have a target
				if indentation_level == 0:
					for link in childless_links:
						link.target = node
						links.append(link)
					childless_links = []

			else:
				print ('adding link for: "' + line + '"')
				pp.pprint(nodes[::-1])
				# the source is the last node in the list at one lower indent
				for node in nodes[::-1]:
					if node.indentation_level == indentation_level - 1:
						source_node = node
						break

				link = Link(**{
					'id': 'link-' + str(link_counter),
					'text': line,
					'source': source_node,
					'indentation_level': indentation_level
				})

				links_to_link.append(link)

				link_counter += 1

			print ('----------------------------------------------------------------------------------------------------------------------------')

		story = {
			'nodes': nodes,
			'links': links
		}
		pp.pprint(story)
		return