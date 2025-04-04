from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
class Production(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(255), nullable=False)
    subitem = db.Column(db.String(255), nullable=False)
    subtotal = db.Column(db.Integer, nullable=True)