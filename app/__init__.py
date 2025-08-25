from flask import Flask
from app.routes import main

def create_app():
    app = Flask(__name__)
    app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para sessões
    app.register_blueprint(main)
    return app
