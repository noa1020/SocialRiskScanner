from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from .routes import register_routes


def create_app():
    app = Flask(__name__)
    CORS(app)

    api = Api(app, prefix="/default")
    namespace = api.namespace("")

    register_routes(namespace)

    return app