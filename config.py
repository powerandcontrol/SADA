# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///historico_escolar.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STATIC_URL_PATH = '/static'
    STATIC_FOLDER = 'static'
