from flask import Flask, jsonify, request, redirect, url_for
from flasgger import Swagger, swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from database import Database
from service import Service
import bcrypt
from datetime import timedelta

app = Flask(__name__)
app.config.from_object('config')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=15)
swagger = Swagger(app)
jwt = JWTManager(app)
database = Database(app)
db = database.get_database()
service = Service()

@app.route('/')
def root():
    return redirect(url_for("flasgger.apidocs"))

@app.route("/registro", methods=["POST"])
@swag_from('swagger/registro.yml')
def register_user():
    data = request.get_json()
    
    if not service.valida_dados_usuario(data):
        return jsonify({"msg": "Campos username e password não informados, menores que 5 caracteres ou maiores que 10 caracteres"}), 400

    if database.get_user(data["username"]):
        return jsonify({"msg": "O usuário já existe"}), 403

    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    database.create_user(username=data["username"], password=hashed_password.decode('utf-8'))
    return jsonify({"msg": "Usuário criado com sucesso"}), 201

@app.route("/login", methods=["POST"])
@swag_from('swagger/login.yml')
def login():
    data = request.get_json()

    if not service.valida_dados_usuario(data):
        return jsonify({"msg": "Campos username e password não informados, menores que 5 caracteres ou maiores que 10 caracteres"}), 400

    user = database.get_user(data["username"])

    if user:
        if bcrypt.checkpw(password=data["password"].encode('utf-8'), hashed_password=str.encode(user.password)):
            return jsonify({"access_token": create_access_token(identity=str(user.id))}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/producao/<int:ano>", methods=["GET"])
@jwt_required()
@swag_from('swagger/producao.yml')
def producao(ano):
    OPCAO_PRODUCAO = "02"

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 400

    return service.processa(database, ano, OPCAO_PRODUCAO)


@app.route("/processamento/<int:ano>/<string:subopcao>", methods=["GET"])
@jwt_required()
@swag_from('swagger/processamento.yml')
def processamento(ano, subopcao):
    
    OPCAO_PROCESSAMENTO = "03"
    SUBOPCOES_VALIDAS = ["01", "02", "03", "04"]

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 400

    if str(subopcao) not in SUBOPCOES_VALIDAS:
        return jsonify({"msg": "Subopção inválida"}), 400

    return service.processa(database, ano, OPCAO_PROCESSAMENTO, subopcao)


@app.route("/comercializacao/<int:ano>", methods=["GET"])
@jwt_required()
@swag_from('swagger/comercializacao.yml')
def comercializacao(ano):
    OPCAO_COMERCIALIZACAO = "04"

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 400

    return service.processa(database, ano, OPCAO_COMERCIALIZACAO)

@app.route("/importacao/<int:ano>/<string:subopcao>", methods=["GET"])
@jwt_required()
@swag_from('swagger/importacao.yml')
def importacao(ano, subopcao):
    
    OPCAO_IMPORTACAO = "05"
    SUBOPCOES_VALIDAS = ["01", "02", "03", "04", "05"]

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 400

    if str(subopcao) not in SUBOPCOES_VALIDAS:
        return jsonify({"msg": "Subopção inválida"}), 400

    return service.processa(database, ano, OPCAO_IMPORTACAO, subopcao)


@app.route("/exportacao/<int:ano>/<string:subopcao>", methods=["GET"])
@jwt_required()
@swag_from('swagger/exportacao.yml')
def exportacao(ano, subopcao):
    
    OPCAO_EXPORTACAO = "06"
    SUBOPCOES_VALIDAS = ["01", "02", "03", "04"]

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 400

    if str(subopcao) not in SUBOPCOES_VALIDAS:
        return jsonify({"msg": "Subopção inválida"}), 400

    return service.processa(database, ano, OPCAO_EXPORTACAO, subopcao)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
