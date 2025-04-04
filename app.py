from flask import Flask, jsonify, request
from flasgger import Swagger
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import User, db, Production
from datetime import datetime
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)
app.config.from_object('config')
swagger = Swagger(app)
jwt = JWTManager(app)
db.init_app(app)

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

@app.route("/login", methods=["POST"])
def login():
    """
    Faz login do usuário e retorna um JWT.
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
                password:
                    type: string
    responses:
      200:
        description: Login bem sucedido, retorna JWT
      401:
        description: Credenciais inválidas
    """
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.password == data["password"]:
        # converter o ID para string
        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    """
    Rota protegida por autenticação
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
                password:
                    type: string

    responses:
      200:
        description: Rota protegida acessada com sucesso
      400:
        description: Erro de autenticação
    """
    current_user_id = get_jwt_identity()
    return jsonify({"msg": f"Usuário com ID {current_user_id} acessou a rota protegida"}), 200

@app.route("/production/<int:year>", methods=["GET"])
def production(year):
    """
    Retorna a dados da produção de uvas, vinhos e derivados
    ---
    parameters:
      - in: path
        name: year
        type: integer
        required: true
    responses:
      200:
        description: Dados de produção do ano enviado
      401:
        description: Ano inválido
    """
    if 1970 < year > datetime.now().year:
        jsonify({"msg": "Ano inválido"}), 401


    URL = f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02&ano={year}"
    print(URL)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    data = []

    table = soup.find('table', attrs={'class':'tb_dados'})
    table_header = table.find('thead')
    rows = table_header.find_all('tr')
    for row in rows:
      cols = row.find_all('th')
      cols = [ele.text.strip() for ele in cols]
      data.append([ele for ele in cols if ele]) # Get rid of empty values

    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      data.append([ele for ele in cols if ele]) # Get rid of empty values

    table_footer = table.find('tfoot')
    rows = table_footer.find_all('tr')
    for row in rows:
      cols = row.find_all('td')
      cols = [ele.text.strip() for ele in cols]
      data.append([ele for ele in cols if ele]) # Get rid of empty values

    print(data)

    #print(page.text)

    print("year: ", year)
    return jsonify({"msg": year}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
