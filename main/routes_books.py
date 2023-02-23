"""
This module implements routes for books data in the flask app.
"""

from flask import jsonify, request
from app import app
from main.extentions import db
from main.books import TableBkMetadata, TableBkRatings
from main.helper import helper
from sqlalchemy import func

@app.route('/dbgettop10newestbooks', methods = ['GET'])
def get_top_10_newest_books():
    """This route implements a page that shows data for the top 10
    newest books.

    Returns:
        json: Data is returned in json format.
    """
    allvalues = TableBkMetadata.query \
                .order_by(TableBkMetadata.bk_metadata_year.desc().nulls_last(), TableBkMetadata.bk_metadata_title.asc()) \
                .limit(10).all()
    allvalues_dict = helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetgivenbookdata', methods = ['GET'])
def get_given_book_data():
    """This route implements a page that shows data for a specific book
    that needs to be defined when calling the route.

    Returns:
        json: Data is returned in json format.
    """
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
    """This route implements a page that shows data for top 20 books
    whose name responds to the search word.

    Returns:
        json: Data is returned in json format.
    """
    if request.args['input'] != '':
        search_raw = request.args['input']
        search_term = f'%{search_raw}%'
        allvalues = TableBkMetadata.query \
                    .filter(TableBkMetadata.bk_metadata_title.ilike(search_term)) \
                    .order_by(TableBkMetadata.bk_metadata_title \
                    .ilike(search_term).desc(), TableBkMetadata.bk_metadata_title) \
                    .limit(20).all()
        if len(allvalues) != 0:
            allvalues_dict = helper.dict_helper(allvalues)
            response = jsonify(allvalues_dict)
        else: 
            response = jsonify({'value': 'not available'})
    else: 
        response = jsonify({'value': 'not available'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10highestratedbooks', methods = ['GET'])
def get_top_10_highest_rated_books():
    """This function searches the 10 books with best average rating. 

    Returns:
        json: json with fields item id and rating: for example:
        {
            "115": "5.0000000000000000",
            ...
            "731": "5.0000000000000000",
            "742": "5.0000000000000000"
            }
    """
    best_rated_books = (
    db.session.query(TableBkRatings.bk_ratings_item_id, func.avg(TableBkRatings.bk_ratings_rating).label("avg_rating"))
    .group_by(TableBkRatings.bk_ratings_item_id, TableBkRatings.bk_ratings_rating)
    .order_by(func.avg(TableBkRatings.bk_ratings_rating).desc())
    .limit(10)
    .all()
    )
    best_rated_books_dict = {}
    for book in best_rated_books:
        best_rated_books_dict[book[0]]=book[1]
    response = jsonify(best_rated_books_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

