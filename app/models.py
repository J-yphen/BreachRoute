from . import db

class AppConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setup_complete = db.Column(db.Boolean, default=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))