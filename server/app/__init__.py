from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Namespace

from .database import init_db
from .routes import register_routes
from .services import analyze_text


def create_app():
    app = Flask(__name__)
    CORS(app)

    api = Api(app, title="Shield Akaton API", description="Analyzes social posts for provisional review signals")
    ns = Namespace("default", description="Default namespace")
    api.add_namespace(ns)

    init_db()
    register_routes(ns)

    app.config["ANALYZER"] = analyze_text
    return app
