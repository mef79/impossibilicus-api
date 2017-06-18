from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Node(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
	name = db.Column(db.Text, unique=True)
	content = db.Column(db.PickleType)

	def __init__(self, story_id, content):
		self.story_id = story_id
		self.content = content

	def __repr__(self):
		return '<Node %r>' % self.name

class Link(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
	name = db.Column(db.Text, unique=True)
	content = db.Column(db.PickleType)

	def __init__(self, story_id, content):
		self.story_id = story_id
		self.content = content

	def __repr__(self):
		return '<Link %r>' % self.name

class Story(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text, unique=True)
	nodes = db.relationship('Node', backref='story', lazy='dynamic')
	links = db.relationship('Link', backref='story', lazy='dynamic')

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return '<Story %r>' % self.name
