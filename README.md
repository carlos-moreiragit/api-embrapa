# Projeto Fase 1 5MLET
Este documento contém informações sobre o projeto da API EMBRAPA que fornece dados da Vitivinicultura desde a década de 70 até os dias atuais.

## URL do Projeto
Na URL do projeto você encontrará o Swagger da aplicação para a utilização imediata da API.

https://api-embrapa-phi.vercel.app/

## Funcionalidades
- Autenticação via JWT com senhas hasheadas pelo bcrypt
- A API mantém um cache em banco de dados para que a instabilidade do site não afetem os teses
- A API armazena os resultados das chamadas afim de utilizar essses resultados como o cache do ítem acima
- Todas as funcionalidades do site estão presentes na API, como filtro por ano, tipos de uvas e etc...

# Detalhes Técnicos
- MVP publicado no Vercel em: https://api-embrapa-phi.vercel.app/
- Banco de dados Neon
- Projeto baseado em Flask e Flasgger

![Diagrama overview](/diagramas/tc01_overview.png)

## Pacotes Utilizados
- flask
- flasgger
- Flask-SQLAlchemy
- flask-jwt-extended
- beautifulsoup4
- requests
- psycopg2-binary
- bcrypt

## Executar Localmente
- python -m venv venv
- pip install -r requirements.txt
- python index.py

## Modelo de Dados
![Diagrama do Modelo de Dados](/diagramas/tc01_mer.png)

***
## Utilização
Para utilizar a API é necessário criar um usuário e fazer login, o que retornará um token válido por 7 dias que deverá ser enviado no header das requisições no formato `Bearer <token>`. Veja o diagrama de sequência abaixo:

![Diagrama de Sequência Criação de Usuário e Login](/diagramas/tc01_diagrama_sequencia.png)

## Endpoints
Endpoints para criação de usuário e login:

|Funçao|Endpoint|
| ------ | ------- |
|Registro de Usuário|https://api-embrapa-phi.vercel.app/registro|
|Login|https://api-embrapa-phi.vercel.app/login|

### Registro de Usuário
`Antes de utilizar os serviços da API é necessário registrar um usuário na rota abaixo`

**Endpoint**
https://api-embrapa-phi.vercel.app/registro

**Tipo de Requisição**
POST

**Corpo da Requisição application/json**
***username*** e ***password*** devem conter entre 5 e 10 caracteres.

```json
{
    "username": "",
    "password": ""
}
```

**Response**
***201:***
descrição: Usuário registrado com sucesso
***400:***
descrição: Campos username e password não informados, menores que 5 caracteres ou maiores que 10 caracteres
***403:***
descrição: Usuário já existe
***
### Login
Tendo um usuário cadastrado você deve fazer login para receber um JWT válido por 7 dias, no endpoint abaixo:

**Endpoint**
https://api-embrapa-phi.vercel.app/login

**Tipo de Requisição**
POST

**Corpo da Requisição application/json**
***username*** e ***password*** devem conter entre 5 e 10 caracteres e ser correspondentes às duas credenciais na API.

```json
{
    "username": "",
    "password": ""
}
```

**Response**
***200:***
descrição: Login bem sucedido, retorna JWT
***400:***
descrição: Campos username e password não informados, menores que 5 caracteres ou maiores que 10 caracteres
***401:***
descrição: Credenciais inválidas
***
Abaixo a lista dos endpoints de serviço da API, ou seja, aqueles que retornam dados da EMBRAPA:

![Diagrama de Requisição da API](/diagramas/tc01_diagrama_requisicoes.png)

|Funçao|Endpoint|
| ------ | ------- |
|Comercialização|https://api-embrapa-phi.vercel.app/comercializacao/|
|Exportação|https://api-embrapa-phi.vercel.app/exportacao/|
|Importação|https://api-embrapa-phi.vercel.app/importacao|
|Processamento|https://api-embrapa-phi.vercel.app/processamento|
|Produção|https://api-embrapa-phi.vercel.app/producao|

> Nota: `Todas as rotas de busca de dados necessitam do envio do token de autenticação no header da requisição no formato Bearer <token> no Swagger Caso utilize o Postman, Insomnia ou outros, basta selecionar a aba authorization, Bearer token em auth type colar o valor do token no campo apropriado`

### Comercialização
Esse endpoint retorna os dados de comercialização da EMBRAPA para o ano enviado no path da requisição.

`É necessário ter um usuário cadastrado na API para que você possa criar um token de autenticação válido`

**Endpoint**
https://api-embrapa-phi.vercel.app/comercializacao/{ano}

**Tipo de Requisição**
GET

**Header da Requisição**

Token válido que dever ser obtido no endpoint /login deve ser enviado no header da requisição como exemplificado abaixo:

> Campo: authorization: <token>

***Path da Requisição***

***ano***
Uma data válida a partir de 1970 até os dias atuais.
	
**Response**
***200:***
descrição: Dados de comercialização do ano enviado
***226:***
descrição: Dados enviados do cache local
***400:***
descrição: Ano inválido
***401:***
descrição: Faltando header de autorização
***503:***
descrição: Serviço indisponível, tente mais tarde
***
### Exportação
Esse endpoint retorna os dados de exportação da EMBRAPA para o ano e a subopção enviados no path da requisição.

`É necessário ter um usuário cadastrado na API para que você possa criar um token de autenticação válido`

**Endpoint**
https://api-embrapa-phi.vercel.app/exportacao/{ano}/{subopcao}

**Tipo de Requisição**
GET

**Header da Requisição**

Token válido que dever ser obtido no endpoint /login deve ser enviado no header da requisição como exemplificado abaixo:

> Campo: authorization: <token>

**Path da Requisição**

***ano***
Uma data válida a partir de 1970 até os dias atuais.
***subopcao***
Uma opção válida dentre as seguintes:
01 - Vinhos de mesa
02 - Espumantes
03 - Uvas frescas
04 - Suco de uva

**Response**
***200:***
descrição: Dados de comercialização do ano enviado
***226:***
descrição: Dados enviados do cache local
***400:***
descrição: Ano inválido
***401:***
descrição: Faltando header de autorização
***503:***
descrição: Serviço indisponível, tente mais tarde

### Importação
Esse endpoint retorna os dados de importação da EMBRAPA para o ano e a subopção enviados no path da requisição.

`É necessário ter um usuário cadastrado na API para que você possa criar um token de autenticação válido`

**Endpoint**
https://api-embrapa-phi.vercel.app/importacao/{ano}/{subopcao}

**Tipo de Requisição**
GET

**Header da Requisição**
Token válido que dever ser obtido no endpoint /login deve ser enviado no header da requisição como exemplificado abaixo:

> Campo: authorization: <token>

**Path da Requisição**

***ano***
Uma data válida a partir de 1970 até os dias atuais.
***subopcao***
Uma opção válida dentre as seguintes:
01 - Vinhos de mesa
02 - Espumantes
03 - Uvas frescas
04 - Uvas passas
05 - Suco de uv

**Response**
***200:***
descrição: Dados de comercialização do ano enviado
***226:***
descrição: Dados enviados do cache local
***400:***
descrição: Ano inválido
***401:***
descrição: Faltando header de autorização
***503:***
descrição: Serviço indisponível, tente mais tarde

### Processamento
Esse endpoint retorna os dados de processamento da EMBRAPA para o ano e a subopção enviados no path da requisição.

`É necessário ter um usuário cadastrado na API para que você possa criar um token de autenticação válido`

**Endpoint**
https://api-embrapa-phi.vercel.app/processamento/{ano}/{subopcao}

**Tipo de Requisição**
GET

**Header da Requisição**
Token válido que dever ser obtido no endpoint /login deve ser enviado no header da requisição como exemplificado abaixo:

> Campo: authorization: <token>

**Path da Requisição**

***ano***
Uma data válida a partir de 1970 até os dias atuais.
***subopcao***
Uma opção válida dentre as seguintes:
01 - Viníferas
02 - Americanas e híbridas
03 - Uvas de mesa
04 - Sem classificação

**Response**
***200:***
descrição: Dados de comercialização do ano enviado
***226:***
descrição: Dados enviados do cache local
***400:***
descrição: Ano inválido
***401:***
descrição: Faltando header de autorização
***503:***
descrição: Serviço indisponível, tente mais tarde

### Produção
Esse endpoint retorna os dados de produção da EMBRAPA para o ano enviado no path da requisição.

`É necessário ter um usuário cadastrado na API para que você possa criar um token de autenticação válido`

**Endpoint**
https://api-embrapa-phi.vercel.app/producao/{ano}

**Tipo de Requisição**
GET

**Header da Requisição**
Token válido que dever ser obtido no endpoint /login deve ser enviado no header da requisição como exemplificado abaixo:

> Campo: authorization: <token>

**Path da Requisição**

***ano***
Uma data válida a partir de 1970 até os dias atuais.
	
**Response**
***200:***
descrição: Dados de comercialização do ano enviado
***226:***
descrição: Dados enviados do cache local
***400:***
descrição: Ano inválido
***401:***
descrição: Faltando header de autorização
***503:***
descrição: Serviço indisponível, tente mais tarde
