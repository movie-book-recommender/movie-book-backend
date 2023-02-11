from app import app
from main.extentions import db
from main.usage import TableTest, TableInputTest2
from flask import request
from datetime import datetime

# Test routes

@app.route('/inserttodb', methods = ['GET'])
def insert_data_to_db():
    given_data = request.args['input'] # get data from arguments
    inval = TableTest(input_test_inputvalue=given_data)
    db.session.add(inval)
    db.session.commit()
    return 'thank you'

@app.route('/inserttodbtest', methods = ['GET'])
def insert_data_to_db_new():
#    given_data = request.args['input'] # get data from arguments
#    given_data = [['0293498m290=3', 'm', 290, 3], ['0293498m290=3', 'm', 290, 5]]
#    given_data = [['0293498m290=3', 'm', 290, 3], ['0293498m290=3', 'm', 290, 5]]
#    existing_data = TableInputTest2.query.filter(TableInputTest2.inputtest2_cookie == given_data[0][0])
#    if existing_data != None:
#        TableInputTest2.update.filter(TableInputTest2.inputtest2_cookie==given_data[0][0]).values(inputtest2_row_valid='False')
#        inval = TableInputTest2(inputtest2_cookie=given_data[1][0], inputtest2_document_id=given_data[1][1], inputtest2_item_id=given_data[1][2], inputtest2_users_rating=given_data[1][3], inputtest2_row_valid='True')
#        db.session.add(inval)
#        db.session.commit()
#        return 'updated'

    given_data = ['02934sdf9668m290=5', 'm', 290, 5]
    inval = TableInputTest2(inputtest2_cookie=given_data[0],
                            inputtest2_document_id=given_data[1],
                            inputtest2_item_id=given_data[2],
                            inputtest2_users_rating=given_data[3],
                            inputtest2_input_time=datetime.now())
    db.session.add(inval)
    db.session.commit()

    return 'thank you'
