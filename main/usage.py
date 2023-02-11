from main.extentions import db

# Test classes how to insert usage data into database

class TableTest(db.Model): # Luodaan testitaulu, johon voidaan laittaa jotain
    __tablename__ = 'input_test'
    input_test_inputvalue = db.Column('inputvalue', db.String(250), primary_key=True)

class TableInputTest2(db.Model): # Luodaan testitaulu, johon voidaan laittaa jotain
    __tablename__ = 'input_test2'
    inputtest2_cookie = db.Column('cookie', db.String(250), primary_key=True)
    inputtest2_document_id = db.Column('document_id', db.String(250), primary_key=True)
    inputtest2_item_id = db.Column('item_id', db.Integer)
    inputtest2_users_rating = db.Column('users_rating', db.Integer)
    inputtest2_input_time = db.Column('input_time', db.Date)