SECRET_KEY = "chave secreta"
CACHE_TYPE = "simple"
SWAGGER = {
    "title": "Dados da Vitivinicultura",
    "uiversion": 3,
    }
SQLALCHEMY_DATABASE_URI = "sqlite:///api-embrapa.db"
#SQLALCHEMY_DATABASE_URI = "postgresql://api-embrapa_owner:npg_XAD26xYhaNdo@ep-muddy-smoke-acgyqq0l-pooler.sa-east-1.aws.neon.tech/api-embrapa?sslmode=require"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = "minha chave"