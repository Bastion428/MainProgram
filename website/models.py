from . import db
from flask_login import UserMixin


class MyGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(100), nullable=False)
    developer = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    image = db.Column(db.String(1000))
    score = db.Column(db.Integer)
    play_hours = db.Column(db.Integer)
    own = db.Column(db.Boolean)
    beat = db.Column(db.Boolean)
    review = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    games = db.relationship('MyGame')
