"""
This module outlines the contents of all the tables with data 
regarding user actions.
"""
from main.extentions import db

class TableTest(db.Model):
    """This class outlines structure for a table to test inserting data into 
    database.

    Args:
        db (object): Table contains input values.
    """
    __tablename__ = 'input_test'
    input_test_inputvalue = db.Column('inputvalue', db.String(250), primary_key=True)

class TableInputTest2(db.Model):
    """This class outlines structure for a table to test how to insert
    cookie data into database.

    Args:
        db (object): Table contains cookie data on users' ratings.
    """
    __tablename__ = 'input_test2'
    inputtest2_cookie = db.Column('cookie', db.String(250), primary_key=True)
    inputtest2_document_id = db.Column('document_id', db.String(250), primary_key=True)
    inputtest2_item_id = db.Column('item_id', db.Integer)
    inputtest2_users_rating = db.Column('users_rating', db.Integer)
    inputtest2_input_time = db.Column('input_time', db.Date)
