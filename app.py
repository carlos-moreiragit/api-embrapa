from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from database import Database
from common import common_api

OPCAO_PROCESSAMENTO = "03"
OPCAO_PRODUCAO = "02"

app = Flask(__name__)
app.config.from_object('config')
swagger = Swagger(app)
jwt = JWTManager(app)
database = Database(app)
db = database.get_database()

@app.route("/register", methods=["POST"])
@swag_from('swagger/register.yml')
def register_user():

    data = request.get_json()
    if database.get_user(data["username"]):
        return jsonify({"error": "User already exists"}), 201
    database.create_user(username=data["username"], password=data["password"])
    return jsonify({"message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
@swag_from('swagger/login.yml')
def login():
    data = request.get_json()
    user = database.get_user(data["username"], data["password"])
    if user and user.password == data["password"]:
        # converter o ID para string
        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/protected", methods=["GET"])
@jwt_required()
@swag_from('swagger/protected.yml')
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"msg": f"Usuário com ID {current_user_id} acessou a rota protegida"}), 200

@app.route("/processamento/<int:ano>/<string:subopcao>", methods=["GET"])
@swag_from('swagger/processamento.yml')
def processamento(ano, subopcao):
    # subopcao 01, 02, 03, 04
    return common_api(database, ano, OPCAO_PROCESSAMENTO, subopcao)

@app.route("/producao/<int:ano>", methods=["GET"])
@swag_from('swagger/producao.yml')
def producao(ano):
    return common_api(database, ano, OPCAO_PRODUCAO)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
