"""
This module is implements a Flask application for back-end APIs
in the Movie Book Recommender application.
"""
import os
from os import getenv
from flask import Flask, jsonify, request
from main.extentions import db

def create_app():
    """This function returns a Flask application 
    and SQLAlchemy database.

    Returns:
        object: Flaks application and SQLAlchemy database.
    """
    app = Flask(__name__)
    # Possibly later separate configuration to a separate file

    #app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URL") <- for future use

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]

    # testi: toimii
    print('variable is possibly:')
    print(os.getenv("ACTIONS_CI"))

    if os.getenv("ACTIONS_CI") == True:
        print("App initialization: In GitHUb actions")
    else: 
        print("App initialization: not in GitHub actions")

    # Initiatilize Flask extentions
    db.init_app(app)

    @app.route("/")
    def index():
        return "hello"

    return app
