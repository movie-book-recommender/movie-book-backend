"""
This module is implements a Flask application for back-end APIs
in the Movie Book Recommender application.
"""
import os
from os import getenv
from flask import Flask, jsonify, request
from main.extentions import db
#from flask_cors import CORS # Uncomment when developing with frontend locally

def create_app():
    """This function returns a Flask application 
    and SQLAlchemy database.

    Returns:
        object: Flaks application and SQLAlchemy database.
    """
    app = Flask(__name__)
    #CORS(app) # Uncomment when developing with frontend locally
    # Possibly later separate configuration to a separate file

    #app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URL") <- for future use

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]

    # Initiatilize Flask extentions
    db.init_app(app)

    @app.route("/")
    def index():
        return "hello"

    return app
