# This file is used to create the Flask app instance and configure it.
from flask import Flask
from flask_cors import CORS, cross_origin

def create_app():
    app=Flask(__name__)
    CORS(app)
    # Registrar las rutas
    from .routes import main
    app.register_blueprint(main)
    return app