from flask import Flask
from app.config import Config
from app.extensions import db, csrf
from app.deals.routes import deals_bp

def create_app(config_class=Config):
    app = Flask(__name__)

    #Load settings from config.py
    app.config.from_object(config_class)

    #connect extensions to the app
    db.init_app(app)
    csrf.init_app(app)

    #Register routes
    app.register_blueprint(deals_bp)

    return app