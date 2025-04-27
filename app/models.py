from . import db

class AppConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setup_complete = db.Column(db.Boolean, default=False)
