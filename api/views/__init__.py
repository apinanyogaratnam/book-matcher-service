from flask import Flask
from flask_restful import Api

from api.controllers import HealthCheck, Home, Match


def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Initialize Config
    app.config.from_pyfile("../../config.py")

    # Register Resources
    api.add_resource(HealthCheck, "/healthcheck")
    api.add_resource(Home, "/")
    api.add_resource(Match, "/match")

    return app
