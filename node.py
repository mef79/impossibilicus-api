from util import debug_trunc

class Node(object):
	def __init__(self, **kwargs):
		self.id = kwargs.get('id') if 'id' in kwargs else None
		self.text = kwargs.get('text') if 'text' in kwargs else None
		self.indent_level = kwargs.get('indent_level') if 'indent_level' in kwargs else None

	def __iter__(self):
		yield 'id', self.id
		yield 'content', self.text

	# for debugging
	# def __repr__(self):
	# 		return "{" + str(self.indent_level) + "/" + debug_trunc(self.text) + "}"