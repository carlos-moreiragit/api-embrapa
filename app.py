from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)
app.config.from_object('config')
swagger = Swagger(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route("/register", methods=["POST"])
def register_user():
    """
    Registra um novo usuário.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
            type: object
            properties:
                username:
                    type: string
                    required: true
                password:
                    type: string
                    required: true
    responses:
      201:
        description: Usuário registrado com sucesso
      400:
        description: Usuário já existe
          
    """
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "User already exists"}), 201
    new_user = User(username=data["username"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201
