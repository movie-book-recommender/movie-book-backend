from app import app
from main.books import TableBkMetadata
from flask import jsonify, request
from main.helper import Helper

@app.route('/dbgettop10newestbooks', methods = ['GET'])
def get_top_10_newest_books():
    allvalues = TableBkMetadata.query \
                .order_by(TableBkMetadata.bk_metadata_year.desc().nulls_last(), TableBkMetadata.bk_metadata_title.asc()) \
                .limit(10).all()
    allvalues_dict = Helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetgivenbookdata', methods = ['GET'])
def get_given_book_data():
    if request.args['bookid'] != '':
        if request.args['bookid'].isdigit():
            bookid = int(request.args['bookid'])
            allvalues = TableBkMetadata.query \
                        .filter_by(bk_metadata_item_id = bookid).first()
            if allvalues is not None: 
                response = jsonify(allvalues.object_to_dictionary())
            else: 
                response = jsonify({'value': 'not available'})
        else: 
            response = jsonify({'value': 'not available'})
    else:
        response = jsonify({'value': 'not available'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbsearchbooksbyname', methods = ['GET'])
def search_books_by_name_top_20():
    search_raw = request.args['input']
    search_term = f'%{search_raw}%'
    allvalues = TableBkMetadata.query \
                .filter(TableBkMetadata.bk_metadata_title.ilike(search_term)) \
                .order_by(TableBkMetadata.bk_metadata_title \
                .ilike(search_term).desc(), TableBkMetadata.bk_metadata_title) \
                .limit(20).all()
    allvalues_dict = Helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
