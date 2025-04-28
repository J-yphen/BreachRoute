from . import db
from sqlalchemy import Enum
from flask_login import UserMixin

class AppConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setup_complete = db.Column(db.Boolean, default=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_path = db.Column(db.Text, unique=True, nullable=False)
    path_visible = db.Column(db.Boolean, default=True, nullable=False)
    filename = db.Column(db.Text, nullable=False)
    response_type = db.Column(Enum('template', 'file', name='response_type_enum'), nullable=False)
