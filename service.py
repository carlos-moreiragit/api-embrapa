from flask import jsonify
import requests
from parser import Parser
from datetime import datetime


class Service:
        
    SITE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?"
    ANO_LIMITE_INFERIOR = 1970
    TAMANHO_MINIMO_SENHA = 5
    TAMANHO_MAXIMO_SENHA = 10
    TAMANHO_MINIMO_USUARIO = 5
    TAMANHO_MAXIMO_USUARIO = 10

    def processa(self, database, ano, opcao, subopcao=None):
        """Implementa a lógica de processamento das chamadas de serviço da API. Se o site da EMBRAPA estiver disponível será feito o
        scraping, caso contrário será returnado conteúdo do cache como resposta.
        
        Keyword arguments:
        database -- o banco de dados da aplicação
        ano -- o ano usado como base da request
        opcao -- a opção que determina o tipo de dado: importação, exportação e etc...
        subopcao -- representa a subopção entre os tipos de uvas, vinhos e etc...
        """
        
        # recupera o registro correspondente no banco
        content = database.get_persisted_content(opcao, subopcao, ano)

        # monta a URL para chamada no site da EMBRAPA
        if opcao == "02" or opcao == "04":
            url = f"{self.SITE_URL}&ano={ano}&opcao=opt_{opcao}"
        else:
            url = f"{self.SITE_URL}&ano={ano}&opcao=opt_{opcao}&subopcao=subopt_{subopcao}"

        # caso o site esteja disponível faz o scraping
        try:
            requests.get(url)
            parser = Parser(requests.get(url))
            data = parser.parse()

            if content:
                database.update_content(content.id, data)
            else:
                database.persist_content(opcao, subopcao, ano, data)
            
            return jsonify({"msg": data}), 200
        
        except(AttributeError, KeyError) as e:
            return jsonify({"msg": "Serviço indisponível, tente mais tarde."}), 503
        # caso o site esteja indisponível e exista conteúdo em banco para a request solicidada, o cache será enviado como resposta
        except requests.exceptions.RequestException as e:

            if content:
                return jsonify({"msg": content.content}), 226

            # se não houver dados em cache e o site da EMBRAPA estiver fora do ar, retorna HTTP 503
            return jsonify({"msg": "Serviço indisponível, tente mais tarde."}), 503
                

    def valida_data(self, ano):
        if not (self.ANO_LIMITE_INFERIOR <= ano <= datetime.now().year):
            print(self.ANO_LIMITE_INFERIOR <= ano <= datetime.now().year)
            return False
        
        return True

    def valida_dados_usuario(self, data):

        try:
            username = data["username"]
            password = data["password"]
            if not (self.TAMANHO_MINIMO_USUARIO <= len(username) <= self.TAMANHO_MAXIMO_USUARIO) or not (self.TAMANHO_MINIMO_SENHA <= len(password) <= self.TAMANHO_MAXIMO_SENHA):
                return False

        except(KeyError) as e:
            return False

        return True
