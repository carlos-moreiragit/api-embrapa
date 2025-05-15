from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from database import Database
from service import Service

app = Flask(__name__)
app.config.from_object('config')
swagger = Swagger(app)
jwt = JWTManager(app)
database = Database(app)
db = database.get_database()
service = Service()

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

@app.route("/protected", methods=["POST"])
@jwt_required()
@swag_from('swagger/protected.yml')
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({"msg": f"Usuário com ID {current_user_id} acessou a rota protegida"}), 200

@app.route("/producao/<int:ano>", methods=["GET"])
@swag_from('swagger/producao.yml')
def producao(ano):
    OPCAO_PRODUCAO = "02"

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 401

    return service.processa(database, ano, OPCAO_PRODUCAO)


@app.route("/processamento/<int:ano>/<string:subopcao>", methods=["GET"])
@swag_from('swagger/processamento.yml')
def processamento(ano, subopcao):
    
    OPCAO_PROCESSAMENTO = "03"
    SUBOPCOES_VALIDAS = ["01", "02", "03", "04"]

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 401

    if str(subopcao) not in SUBOPCOES_VALIDAS:
        return jsonify({"msg": "Subopção inválida"}), 401

    return service.processa(database, ano, OPCAO_PROCESSAMENTO, subopcao)


@app.route("/comercializacao/<int:ano>", methods=["GET"])
@swag_from('swagger/comercializacao.yml')
def comercializacao(ano):
    OPCAO_COMERCIALIZACAO = "04"

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 401

    return service.processa(database, ano, OPCAO_COMERCIALIZACAO)

@app.route("/importacao/<int:ano>/<string:subopcao>", methods=["GET"])
@swag_from('swagger/importacao.yml')
def importacao(ano, subopcao):
    
    OPCAO_IMPORTACAO = "05"
    SUBOPCOES_VALIDAS = ["01", "02", "03", "04", "05"]

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 401

    if str(subopcao) not in SUBOPCOES_VALIDAS:
        return jsonify({"msg": "Subopção inválida"}), 401

    return service.processa(database, ano, OPCAO_IMPORTACAO, subopcao)


@app.route("/exportacao/<int:ano>/<string:subopcao>", methods=["GET"])
@swag_from('swagger/exportacao.yml')
def exportacao(ano, subopcao):
    
    OPCAO_EXPORTACAO = "06"
    SUBOPCOES_VALIDAS = ["01", "02", "03", "04"]

    if not service.valida_data(ano):
        jsonify({"msg": "Ano inválido"}), 401

    if str(subopcao) not in SUBOPCOES_VALIDAS:
        return jsonify({"msg": "Subopção inválida"}), 401

    return service.processa(database, ano, OPCAO_EXPORTACAO, subopcao)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
