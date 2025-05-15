from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Database():
    def __init__(self, app):
        db.init_app(app)

    def get_database(self):
        return db
    
    def persist_content(self, option, suboption, year, data):
        new_content = Content(option=option, suboption=suboption, year=year, content=str(data))
        db.session.add(new_content)
        db.session.commit()

    def update_content(self, id, data):
        content = Content.query.filter_by(id=id).first()
        content.content = str(data)
        db.session.commit()

    def get_persisted_content(self, option, suboption, year):
        content = Content.query.filter_by(option=option, suboption=suboption, year=year).first()
        return content
    
    def get_user(self, username, password=None):
        if password:
            user = User.query.filter_by(username=username, password=password).first()
        else:
            user = User.query.filter_by(username=username).first()
        return user
    
    def create_user(self, username, password):
        new_user = User(username=username, password=password)
        db.session.add(new_user)
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