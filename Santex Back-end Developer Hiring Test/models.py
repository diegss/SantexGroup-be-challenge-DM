from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(10), unique=True)
    area_name = db.Column(db.String(100))

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tla = db.Column(db.String(10))
    short_name = db.Column(db.String(100))
    area_name = db.Column(db.String(100))
    address = db.Column(db.String(200))
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.id'))

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    position = db.Column(db.String(50))
    date_of_birth = db.Column(db.String(20))
    nationality = db.Column(db.String(100))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    goals = db.Column(db.Integer, nullable=True)

class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_of_birth = db.Column(db.String(20))
    nationality = db.Column(db.String(100))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))