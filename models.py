from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(255), nullable=False)
    suboption = db.Column(db.String(255), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)