from flask import jsonify
import requests
from parser import Parser
from datetime import datetime


class Service:
        
    SITE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?"
    ANO_LIMITE_INFERIOR = 1970

    def processa(self, database, ano, opcao, subopcao=None):
        
        content = database.get_persisted_content(opcao, subopcao, ano)

        print(content)

        if opcao == "02" or opcao == "04":
            url = f"{self.SITE_URL}&ano={ano}&opcao=opt_{opcao}"
        else:
            url = f"{self.SITE_URL}&ano={ano}&opcao=opt_{opcao}&subopcao=subopt_{subopcao}"

        try:
            requests.get(url)
            parser = Parser(requests.get(url))
            data = parser.parse()

            if content:
                database.update_content(content.id, data)
            else:
                database.persist_content(opcao, subopcao, ano, data)
            
            print("Conteúdo do SITE recuperado")
            return jsonify({"msg": data}), 200
        
        except(AttributeError, KeyError) as e:
            return jsonify({"msg": "SServiço indisponível, tente mais tarde."}), 503
        
        except requests.exceptions.RequestException as e:

            if content:
                print("Conteúdo do BANCO DE DADOS recuperado")
                return jsonify({"msg": content.content}), 200

            return jsonify({"msg": "Serviço indisponível, tente mais tarde."}), 503
                

    def valida_data(self, ano):
        if self.ANO_LIMITE_INFERIOR < ano > datetime.now().year:
            return False
        
        return True
