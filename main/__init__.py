import os
from os import getenv
from flask import Flask, jsonify, request
from main.extentions import db

#from flask_sqlalchemy import SQLAlchemy # siirrettävä db.py:n

def create_app():
    app = Flask(__name__)
    # Possibly later separate configuration to a separate file
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv("DATABASE_URL")

    # Initiatilize Flask extentions
    db.init_app(app)

#    db = SQLAlchemy(app) # siirrä db.py:n

    @app.route("/")
    def index():
        return "hello"

    return app

