# Projeto Fase 1 5MLET
Este documento contém informações sobre a projeto da API EMBRAPA que fornece dados da Dados da Vitivinicultura desde a década de 70 até os dias atuais

## URL do MVP
https://api-embrapa-k7b6lkl5p-carlos-projects-42c43b32.vercel.app/


## Endpoints


Endpoints para criação de usuário e login:

# Registro de Usuário
https://api-embrapa-k7b6lkl5p-carlos-projects-42c43b32.vercel.app/apidocs/#/default/post_register

# Login
https://api-embrapa-k7b6lkl5p-carlos-projects-42c43b32.vercel.app/apidocs/#/default/post_login


Os endpoints abaixo são os que trazem os dados da EMBRAPA:

# Comercialização
https://api-embrapa-k7b6lkl5p-carlos-projects-42c43b32.vercel.app/apidocs/#/default/get_comercializacao__ano_

# Exportação
https://api-embrapa-k7b6lkl5p-carlos-projects-42c43b32.vercel.app/apidocs/#/default/get_exportacao__ano___subopcao_

# Importação
https://api-embrapa-k7b6lkl5p-carlos-projects-42c43b32.vercel.app/apidocs/#/default/get_importacao__ano___subopcao_

# Processamento
https://api-embrapa-k7b6lkl5p-carlos-projects-42c43b32.vercel.app/apidocs/#/default/get_processamento__ano___subopcao_

# Produção
https://api-embrapa-k7b6lkl5p-carlos-projects-42c43b32.vercel.app/apidocs/#/default/get_producao__ano_


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
- psycopg2-binary
- bcrypt
