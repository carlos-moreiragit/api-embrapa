from flask import jsonify
from datetime import datetime
import requests
from parser import Parser

def common_api(database, ano, opcao, subopcao=None):

    VALID_OPTIONS = ["02", "03", "04", "05", "06"]
    VALID_SUBOPTIONS = ["01", "02", "03", "04", "05"]
    SITE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?"

    if 1970 < ano > datetime.now().year:
        jsonify({"msg": "Ano inválido"}), 401

    if str(opcao) not in VALID_OPTIONS:
        return jsonify({"msg": "Opção inválida"}), 401
    
    if subopcao and str(subopcao) not in VALID_SUBOPTIONS:
        return jsonify({"msg": "Subopção inválida"}), 401

    content = database.get_persisted_content(opcao, subopcao, ano)
    if content:
        return jsonify({"msg": content.content}), 200

    if opcao == "02" or opcao == "04":
      url = f"{SITE_URL}&ano={ano}&opcao=opt_{opcao}"
    else:
      url = f"{SITE_URL}&ano={ano}&opcao=opt_{opcao}&subopcao=subopt_{subopcao}"

    parser = Parser(requests.get(url))
    data = parser.parse()

    database.persist_content(opcao, subopcao, ano, data)
    
    return jsonify({"msg": data}), 200

