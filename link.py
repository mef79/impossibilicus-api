
class Link:
	def __init__(self, **kwargs):
		self.id = kwargs.get('id') if 'id' in kwargs else None
		self.text = kwargs.get('text') if 'text' in kwargs else None
		self.source = kwargs.get('source') if 'source' in kwargs else None
		self.target = kwargs.get('target') if 'target' in kwargs else None
		self.indentation_level = kwargs.get('indentation_level') if 'indentation_level' in kwargs else None

	def __repr__(self):
		if self.target:
			return "{" + str(self.indentation_level) + "/" + self.source.text[:25] + "...} => " + \
				"{" + self.text[:25] + "...} => " + \
				"{" + self.target.text[:25] + "...}"
		else:
			return "{" + str(self.indentation_level) + "/" + self.source.text[:35] + "...} => " + \
				"{" + self.text[:25] + "...} => " + \
				"{no target}"