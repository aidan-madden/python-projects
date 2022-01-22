from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(200))
	created_at = db.Column(db.DateTime, server_default=db.func.now())
	updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

class Team(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	full_name = db.Column(db.String(80))
	abbreviation = db.Column(db.String(80))
	nickname = db.Column(db.String(80))
	city = db.Column(db.String(80))
	logo = db.Column(db.String(400))
	conf_name = db.Column(db.String(80))
	div_name = db.Column(db.String(80))
	players = db.relationship('Player', backref='author', lazy=True)	

class Player(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	firstName = db.Column(db.String(80))
	lastName = db.Column(db.String(80))
	h = db.Column(db.String(80))
	weight = db.Column(db.Integer)
	country = db.Column(db.String(80))
	college = db.Column(db.String(80))
	years_pro = db.Column(db.String(80))
	position = db.Column(db.String(80))
	jersey = db.Column(db.String(80))
	team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False) 
