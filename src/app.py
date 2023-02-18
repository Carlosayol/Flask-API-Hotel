from flask import Flask
import os

from src.routes.hotel import create_blueprint
from src.database import mongo


def create_app():
    """
    Generate flask object
    returns: Flask instace
    """
    app = Flask(__name__)
    app.secret_key = os.environ.get("APP_SECRET_KEY")
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
    mongo.init_app(app)
    app.register_blueprint(create_blueprint(mongo), url_prefix="/api/v1")

    return app
