from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Database():
    def __init__(self, app):
        db.init_app(app)

    def get_database(self):
        return db
    
    def record_content(self, option, suboption, year, data):
        new_content = Content(option=option, suboption=suboption, year=year, content=str(data))
        db.session.add(new_content)
        db.session.commit()
    
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