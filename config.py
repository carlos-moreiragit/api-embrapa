SECRET_KEY = "chave secreta"
CACHE_TYPE = "simple"
SWAGGER = {
    "title": "Dados da Vitivinicultura a partir de 1970 até os dias atuais.",
    "uiversion": 3,
    }
#SQLALCHEMY_DATABASE_URI = "sqlite:///api-embrapa.db"
SQLALCHEMY_DATABASE_URI = "postgresql://api-embrapa_owner:npg_sZA7MTpPHvJ3@ep-restless-unit-acypb0d7-pooler.sa-east-1.aws.neon.tech/api-embrapa?sslmode=require"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = "29348572fhjkasrfghklejryhtwi345outhkjg"