from util import debug_trunc

class Link(object):
	def __init__(self, **kwargs):
		self.id = kwargs.get('id') if 'id' in kwargs else None
		self.text = kwargs.get('text').strip() if 'text' in kwargs else None
		self.source = kwargs.get('source') if 'source' in kwargs else None
		self.target = kwargs.get('target') if 'target' in kwargs else None
		self.indent_level = kwargs.get('indent_level') if 'indent_level' in kwargs else None

	def __iter__(self):
		yield 'id', self.id
		yield 'text', self.text
		yield 'source', dict(self.source)
		yield 'target', dict(self.target)

	# for debugging
	# def __repr__(self):
	# 	if self.target:
	# 		return "{" + debug_trunc(self.source.text) + "} => " + \
	# 			"{" + debug_trunc(self.text) + "} => " + \
	# 			"{" + debug_trunc(self.target.text) + "}"
	# 	else:
	# 		return "{" + debug_trunc(self.source.text) + "} => " + \
	# 			"{" + debug_trunc(self.text) + "} => " + \
	# 			"{no target}"