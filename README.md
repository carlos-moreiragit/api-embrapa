# Projeto Fase 1 5MLET
Este documento contém informações sobre a projeto da API EMBRAPA que fornece dados da Dados da Vitivinicultura desde a década de 70 até os dias atuais

## Endpoints


## Funcionalidades
- Autenticação via JWT com senhas hasheadas pelo bcrypt
- A API mantém um cache em banco de dados para que a instabilidade do site não afetem os teses
- A API armazena os resultados das chamadas afim de utilizar essses resultados como o cache do ítem acima
- Todas as funcionalidades do site estão presentes na API, como filtro por ano, tipos de uvas e etc...

# Detalhes Técnicos

## Pacotes Utilizados
- flask
- flasgger
- Flask-SQLAlchemy
- flask-jwt-extended
- beautifulsoup4
- requests
- psycopg2
- bcrypt
