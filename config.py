import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-votaciones-2025')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///votaciones.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
