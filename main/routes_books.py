"""
This module implements routes for books data in the flask app.
"""

import os
from os import getenv
import json
from flask import jsonify, request
from sqlalchemy.sql import text
from app import app
from main.extentions import db
from main.books import TableBkMetadata, TableBkSimilarBooks, TableBkSimilarMovies
from main.movies import TableMovieTmdbDataFull
from main.helper import helper
from main.recommendations import recommendations

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
    search_raw = request.args['input']
    search_term = f'%{search_raw}%'
    allvalues = TableBkMetadata.query \
                .filter(TableBkMetadata.bk_metadata_title.ilike(search_term)) \
                .order_by(TableBkMetadata.bk_metadata_title \
                .ilike(search_term).desc(), TableBkMetadata.bk_metadata_title) \
                .limit(20).all()
    allvalues_dict = helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10highestratedbooks', methods = ['GET'])
def get_top_10_highest_rated_books():
    """This function searches the 10 books with best average rating.

    Returns:
        json:
    """
    sql = """SELECT M.authors, M.description, M.img, M.item_id, M.lang, M.title, M.url, M.year, T.avg_rating
    FROM (SELECT item_id, AVG(rating) as avg_rating
            FROM bk_ratings
            GROUP BY item_id)
            T
            JOIN bk_metadata M ON M.item_id = T.item_id
    ORDER BY T.avg_rating DESC
    LIMIT 10"""
    best_rated_books = (
        db.session.execute(text(sql))
        ).fetchall()
    best_rated_books_list = []
    for result in best_rated_books:
        result = {"authors":result.authors,
                  "description": result.description,
                  "img":result.img,
                  "item_id":result.item_id,
                  "lang":result.lang,
                  "title": result.title,
                  "url":result.url,
                  "year":result.url,
                  "avg_rating": result.avg_rating}
        best_rated_books_list.append(result)
    response = response = jsonify(best_rated_books_list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetforgivenbookrecommendedbooks', methods = ['GET'])
def get_for_given_book_recommended_books():
    """This route implements a page that lists the recommended 250 books for
    a given books that needs to be defined when calling the route.
    """
    if request.args['bookid'] != '':
        if request.args['bookid'].isdigit():
            bookid = int(request.args['bookid'])
            allvalues = TableBkSimilarBooks.query \
                            .filter_by(bk_similar_books_item_id = bookid) \
                            .order_by(TableBkSimilarBooks.bk_similar_books_similarity_score.desc()) \
                            .offset(1) \
                            .all()
#            print(len(allvalues))
            if len(allvalues) != 0:
                allvalues_dict = helper.dict_helper(allvalues)
                response = jsonify(allvalues_dict)
            else:
                response = jsonify({'value': 'not available'})
        else:
            response = jsonify({'value': 'not available'})
    else:
        response = jsonify({'value': 'not available'})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetforgivenbookrecommendedbooksalldata', methods = ['GET'])
def get_for_given_book_recommended_books_all_data():
    """This route implements a page that lists the recommended 20 books and their key data for
    a given book that needs to be defined when calling the route

    Returns:
        json: data is returned in json format.
    """
    if request.args['bookid'] != '':
        if request.args['bookid'].isdigit():
            bookid = int(request.args['bookid'])
            allvalues = db.session.query(TableBkMetadata, TableBkSimilarBooks) \
                            .join(TableBkSimilarBooks, TableBkSimilarBooks.bk_similar_books_similar_item_id == TableBkMetadata.bk_metadata_item_id) \
                            .filter_by(bk_similar_books_item_id = bookid) \
                            .order_by(TableBkSimilarBooks.bk_similar_books_similarity_score.desc()) \
                            .offset(1) \
                            .limit(20).all()
            if len(allvalues) != 0:
                allvalues_dict = []
                for value in allvalues:
                    dict_1 = value.TableBkMetadata.object_to_dictionary()
                    dict_2 = value.TableBkSimilarBooks.object_to_dictionary()
                    dict_1.update(dict_2)
                    allvalues_dict.append(dict_1)
                response = jsonify(allvalues_dict)
            else:
                response = jsonify({'value': 'not available'})
        else:
            response = jsonify({'value': 'not available'})
    else:
        response = jsonify({'value': 'not available'})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetrecommendedmoviesforgivenbook', methods = ['GET'])
def get_recommended_movies_for_given_book():
    """This route implements a page that lists all the recommended movies for
    a given book that needs to be defined when calling the route.
    It returns all the movies that have been recommended for a given book.
    """
    if request.args['bookid'] != '':
        if request.args['bookid'].isdigit():
            bookid = int(request.args['bookid'])
            allvalues = TableBkSimilarMovies.query \
                            .filter_by(bk_similar_movies_item_id = bookid) \
                            .order_by(TableBkSimilarMovies.bk_similar_movies_similarity_score.desc()) \
                            .all()
            print(len(allvalues))
            if len(allvalues) != 0:
                allvalues_dict = helper.dict_helper(allvalues)
                response = jsonify(allvalues_dict)
            else:
                response = jsonify({'value': 'not available'})
        else:
            response = jsonify({'value': 'not available'})
    else:
        response = jsonify({'value': 'not available'})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetrecommendedmoviesalldataforgivenbook', methods = ['GET'])
def get_recommended_movies_all_data_for_given_book():
    """This route implements a page that lists a limited number of recommended movies
    and their key data for a given book that needs to be defined when calling the route.

    Returns:
        json: data is returned in json format.
    """
    if request.args['bookid'] != '':
        if request.args['bookid'].isdigit():
            bookid = int(request.args['bookid'])
            allvalues = db.session.query(TableMovieTmdbDataFull, TableBkSimilarMovies) \
                            .join(TableBkSimilarMovies, TableBkSimilarMovies.bk_similar_movies_similar_item_id == TableMovieTmdbDataFull.movie_tmdb_data_full_movieid) \
                            .filter_by(bk_similar_movies_item_id = bookid) \
                            .order_by(TableBkSimilarMovies.bk_similar_movies_similarity_score.desc()) \
                            .limit(20).all()
            if len(allvalues) != 0:
                allvalues_dict = []
                for value in allvalues:
                    dict_1 = value.TableMovieTmdbDataFull.object_to_dictionary()
                    dict_2 = value.TableBkSimilarMovies.object_to_dictionary()
                    dict_1.update(dict_2)
                    allvalues_dict.append(dict_1)
                response = jsonify(allvalues_dict)
            else:
                response = jsonify({'value': 'not available'})
        else:
            response = jsonify({'value': 'not available'})
    else:
        response = jsonify({'value': 'not available'})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbsearchbooksbyauthor', methods = ['GET'])
def get_books_by_author():
    """This route implements a page that shows data for top 20 books
    whose author match to the search word.

    Returns:
        json: Data is returned in json format.
    """
    search_raw = request.args['input']
    search_term = f'{search_raw}%'
    allvalues = TableBkMetadata.query \
                .filter(TableBkMetadata.bk_metadata_authors.ilike(search_term)) \
                .order_by(TableBkMetadata.bk_metadata_authors, TableBkMetadata.bk_metadata_title) \
                .limit(20).all()
    allvalues_dict = helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/dbgetpersonalbookrecommendations", methods = ['GET'])
def get_personal_book_recommendations():
    """
    This route implements a page that lists a limited number (10) of recommended
    books and they key data based on users personal preference.
    Returns:
        json: data is returned in json format.
    """
    if os.getenv("ACTIONS_CI") == "is_in_github":
        print("Book route: In GitHUb actions")
        response = jsonify({'value': 'not available'})
    else:
        print("Book route: not in GitHub actions")

        response = jsonify({'value' : 'not available'})
    #   de-bugging
        if request.args['ratings'] != '':
            cookie_raw = request.args['ratings']
            cookie = json.loads(cookie_raw)
            ratings = helper.ratings_helper(cookie)
            if ratings is False:
                response = jsonify({'value' : 'not available'})
            else:
                results = recommendations.get_book_recommendations(ratings, 10)
                all_values = []
                for result in results:
                    value = TableBkMetadata.query \
                            .filter_by(bk_metadata_item_id = result).first()
                    all_values.append(value)
                allvalues_dict = helper.dict_helper(all_values)
                response = jsonify(allvalues_dict)
        else:
            response = jsonify({'value': 'not available'})

    response.headers.add('Access-Control-Allow-Origin', '*')

#    ratings = {"movies" : [{"item_id" : 1270, "rating" : 4}, # Back to the Future
#                           {"item_id" : 5445, "rating" : 5}, # Minority Report
#                           {"item_id" : 7361, "rating" : 1}], # Eternal Sunshine of the Spotless Mind
#               "books" : [{"item_id" : 150259, "rating" : 4}, # Stephen King - IT
#                          {"item_id" : 3230869, "rating" : 3}]} # Stephen King -Misery
#
#    results = recommendations.get_book_recommendations(ratings, 10) # call algorithm function to form recommendations
#    all_values = []
#    for result in results:
#        value = TableBkMetadata.query \
#                .filter_by(bk_metadata_item_id = result).first()
#        all_values.append(value) # add result to a list
#    allvalues_dict = helper.dict_helper(all_values) # Convert list to a dict
#    response = jsonify(allvalues_dict) # Turn dict to json
#
#    response.headers.add('Access-Control-Allow-Origin', '*') # Add correct headers
#
    return response
