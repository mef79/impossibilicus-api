
class Node:
	def __init__(self, **kwargs):
		self.id = kwargs.get('id') if 'id' in kwargs else None
		self.text = kwargs.get('text') if 'text' in kwargs else None
		self.indentation_level = kwargs.get('indentation_level') if 'indentation_level' in kwargs else None

	def __repr__(self):
			return "{" + str(self.indentation_level) + "/" + self.text[:25] + "...}"