import signal
import time

class Timeout():
	"""Timeout class using ALARM signal."""
	class Timeout(Exception):
		pass

	def __init__(self, sec):
		self.sec = sec

	def __enter__(self):
		signal.signal(signal.SIGALRM, self.raise_timeout)
		signal.alarm(self.sec)

	def __exit__(self, *args):
		signal.alarm(0)    # disable alarm

	def raise_timeout(self, *args):
		raise Timeout.Timeout()

def validate(data):
	assert 'name' in data
	assert 'nodes' in data
	assert 'links' in data
	assert 'node_counter' in data
	assert 'link_counter' in data
	return data

def error(message):
	return {'error': message}

def serializable(story):
	story['_id'] = str(story['_id'])

def debug_trunc(s):
	t = s[:25] + '...'
	if len(t) < 28:
		t += (28 - len(t)) * '.'
	return t