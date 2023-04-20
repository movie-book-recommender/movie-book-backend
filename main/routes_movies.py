"""
This module implements routes for movies data in the flask app.
"""

from datetime import date
import json
from flask import jsonify, request
from sqlalchemy import func
from app import app
from main.extentions import db
from main.movies import TableMovieTmdbDataFull, TableMvMetadataUpdated, TableMvTags, TableMvSimilarMovies, TableMvSimilarBooks
from main.books import TableBkMetadata
from main.helper import helper
from main.recommendations import recommendations

@app.route('/dbgettags', methods = ['GET'])
def gettablevalues():
    """This route implements a page that shows data for tags.

    Returns:
        json: Data is returned in json format.
    """
    allvalues = TableMvTags.query.all()
    allvalues_dict = helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetonemoviedata', methods = ['GET'])
def get_one_movie_data():
    """This route implements a page that shows data for one specific movie.
    Route is for testing only.

    Returns:
        json: Data is returned in json format.
    """
    allvalues = TableMovieTmdbDataFull.query.first()
    response = jsonify(allvalues.object_to_dictionary())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetgivenmoviedata_test', methods = ['GET'])
def get_given_movie_data_test():
    """This route implements a page that shows data for one specific movie with
    a defined id. Route is for testing only.

    Returns:
        json: Data is returned in json format.
    """
    allvalues = TableMovieTmdbDataFull.query \
                .filter_by(movie_tmdb_data_full_movieid = 6).first()
    response = jsonify(allvalues.object_to_dictionary())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetgivenmoviedata', methods = ['GET'])
def get_given_movie_data():
    """This route implements a page that shows data for one specific movie
    that needs to be defined when calling the route.

    Returns:
        json: Data is returned in json format.
    """
    if request.args['movieid'] != '':
        if request.args['movieid'].isdigit():
            movieid = int(request.args['movieid'])
            allvalues = TableMovieTmdbDataFull.query \
                        .filter_by(movie_tmdb_data_full_movieid = movieid).first()
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

@app.route('/dbgettop10moviesbyyear', methods = ['GET'])
def get_top_10_movies_by_year():
    """This route implements a page that shows data for top 10 movies for a year
    that needs to be defined when calling the route.

    Returns:
        json: Data is returned in json format.
    """
    if request.args['year'] != '':
        if request.args['year'].isdigit():
            year_value = int(request.args['year'])
            allvalues = TableMovieTmdbDataFull.query.filter(db.extract('year',
                                TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate) == year_value) \
                                .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_revenue.desc().nulls_last()) \
                                .limit(10).all()
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

@app.route('/dbgettop10newestpublishedmovies', methods = ['GET'])
def get_top_10_newest_published_movies():
    """This route implements a page that shows data for last 10 published movies.

    Returns:
        json: Data is returned in json format.
    """
    date_value = date.today()
    allvalues = TableMovieTmdbDataFull.query \
                    .filter(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate<date_value) \
                    .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate.desc().nulls_last()) \
                    .limit(10).all()
    allvalues_dict = helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10oldestmovies', methods = ['GET'])
def get_top_10_oldest_movies():
    """This route implements a page that shows data for oldest 10 movies.

    Returns:
        json: Data is returned in json format.
    """
    allvalues = TableMovieTmdbDataFull.query \
                    .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate.asc()) \
                    .limit(10).all()
    allvalues_dict = helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbsearchmoviesbyname', methods = ['GET'])
def search_movies_by_name_top_20():
    """This route implements a page that shows data for 20 movies whose
    name is closest to the search term typed by user.

    Returns:
        json: Data is returned in json format.
    """
    search_raw = request.args['input']
    search_term = f'%{search_raw}%'
    allvalues = TableMovieTmdbDataFull.query \
                    .filter(TableMovieTmdbDataFull.movie_tmdb_data_full_title.ilike(search_term)) \
                    .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_title.ilike(search_term).desc(),
                    TableMovieTmdbDataFull.movie_tmdb_data_full_title) \
                    .limit(20).all()
    allvalues_dict = helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbsearchmoviesbysimilarname', methods = ['GET'])
def search_movies_by_similar_name():
    """This route implements a page that shows data for max 100 movies whose
    name is closest to the search term typed by user.

    Returns:
        json: Data is returned in json format.
    """
    search_raw = request.args['input']
    search_term = f'{search_raw}'
    allvalues = db.session.query(TableMovieTmdbDataFull,func.similarity(
        TableMovieTmdbDataFull.movie_tmdb_data_full_title, search_term)) \
            .order_by(func.similarity(
                TableMovieTmdbDataFull.movie_tmdb_data_full_title, search_term) \
            .desc().nulls_last()) \
            .limit(100).all()

    allvalues_dict = []
    for value in allvalues:
        if value[1] > 0.35:
            allvalues_dict.append(value[0].object_to_dictionary())

    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbsearchmoviesbyactor', methods = ['GET'])
def search_movies_by_actor_top_50():
    """This route implements a page that shows data for 50 movies
    whose list of actors icludes term typed by user.

    Returns:
        json: Data is returned in json format.
    """
    search_raw = request.args['input']
    search_term = f'{search_raw}%'
    allvalues = TableMovieTmdbDataFull.query \
                    .filter(TableMovieTmdbDataFull.movie_tmdb_data_full_actors.ilike(search_term)) \
                    .limit(50).all()
    allvalues_dict = helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbsearchmoviesbydirector', methods = ['GET'])
def search_movies_by_director_top_50():
    """This route implements a page that shows data for 50 movies
    whose list of directors icludes term typed by user.

    Returns:
        json: Data is returned in json format.
    """
    search_raw = request.args['input']
    search_term = f'{search_raw}%'
    allvalues = TableMovieTmdbDataFull.query \
                    .filter(TableMovieTmdbDataFull.movie_tmdb_data_full_directors.ilike(search_term)) \
                    .limit(50).all()
    allvalues_dict = helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10highestratedmovies', methods = ['GET'])
def get_top_10_highest_rating_movies():
    """This route implements a page that shows data for 10 movies with
    the highest rating in the database.

    Returns:
        json: Data is returned in json format.
    """
    allvalues = db.session.query(TableMovieTmdbDataFull, TableMvMetadataUpdated) \
                          .join(TableMvMetadataUpdated, TableMvMetadataUpdated.mv_metadata_updated_item_id == TableMovieTmdbDataFull.movie_tmdb_data_full_movieid) \
                          .order_by(TableMvMetadataUpdated.mv_metadata_updated_avgrating.desc().nulls_last(),
                          TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate.desc().nulls_last()) \
                          .limit(10).all()

    allvalues_dict = []
    for value in allvalues:
        dict_1 = value.TableMovieTmdbDataFull.object_to_dictionary()
        dict_2 = value.TableMvMetadataUpdated.object_to_dictionary()
        dict_1.update(dict_2)
        allvalues_dict.append(dict_1)

    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetforgivenmovierecommendedmovies', methods = ['GET'])
def get_for_given_movie_recommended_movies():
    """This route implements a page that lists the recommended 250 movies for
    a given movie that needs to be defined when calling the route.
    """
    if request.args['movieid'] != '':
        if request.args['movieid'].isdigit():
            movieid = int(request.args['movieid'])
            allvalues = TableMvSimilarMovies.query \
                            .filter_by(mv_similar_movies_item_id = movieid) \
                            .order_by(TableMvSimilarMovies.mv_similar_movies_similarity_score.desc()) \
                            .offset(1) \
                            .all()
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

@app.route('/dbgetforgivenmovierecommendedmoviesalldata', methods = ['GET'])
def get_for_given_movie_recommended_movies_all_data():
    """This route implements a page that lists the recommended 20 movies and their key data for
    a given movie that needs to be defined when calling the route

    Returns:
        json: data is returned in json format.
    """
    if request.args['movieid'] != '':
        if request.args['movieid'].isdigit():
            movieid = int(request.args['movieid'])
            allvalues = db.session.query(TableMovieTmdbDataFull, TableMvSimilarMovies) \
                            .join(TableMvSimilarMovies, TableMvSimilarMovies.mv_similar_movies_similar_item_id == TableMovieTmdbDataFull.movie_tmdb_data_full_movieid) \
                            .filter_by(mv_similar_movies_item_id = movieid) \
                            .order_by(TableMvSimilarMovies.mv_similar_movies_similarity_score.desc()) \
                            .offset(1) \
                            .limit(20).all()
            if len(allvalues) != 0:
                allvalues_dict = []
                for value in allvalues:
                    dict_1 = value.TableMovieTmdbDataFull.object_to_dictionary()
                    dict_2 = value.TableMvSimilarMovies.object_to_dictionary()
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

@app.route('/dbgetrecommendedbooksforgivenmovie', methods = ['GET'])
def get_recommended_books_for_given_movie():
    """This route implements a page that lists all the recommended books for
    a given movie that needs to be defined when calling the route.
    It returns all the books that have been recommended for a given movie.
    """
    if request.args['movieid'] != '':
        if request.args['movieid'].isdigit():
            movieid = int(request.args['movieid'])
            allvalues = TableMvSimilarBooks.query \
                            .filter_by(mv_similar_books_item_id = movieid) \
                            .order_by(TableMvSimilarBooks.mv_similar_books_similarity_score.desc()) \
                            .all()
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

@app.route('/dbgetrecommendedbooksalldataforgivenmovie', methods = ['GET'])
def get_recommended_books_all_data_for_given_movie():
    """This route implements a page that lists a limited number of recommended books
    and their key data for a given movie that needs to be defined when calling the route

    Returns:
        json: data is returned in json format.
    """
    if request.args['movieid'] != '':
        if request.args['movieid'].isdigit():
            movieid = int(request.args['movieid'])
            allvalues = db.session.query(TableBkMetadata, TableMvSimilarBooks) \
                            .join(TableMvSimilarBooks, TableMvSimilarBooks.mv_similar_books_similar_item_id == TableBkMetadata.bk_metadata_item_id) \
                            .filter_by(mv_similar_books_item_id = movieid) \
                            .order_by(TableMvSimilarBooks.mv_similar_books_similarity_score.desc()) \
                            .limit(20).all()
            if len(allvalues) != 0:
                allvalues_dict = []
                for value in allvalues:
                    dict_1 = value.TableBkMetadata.object_to_dictionary()
                    dict_2 = value.TableMvSimilarBooks.object_to_dictionary()
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

@app.route("/dbgetpersonalmovierecommendations", methods = ['GET'])
def get_personal_movie_recommendations():
    """
    This route implements a page that lists a limited number (20) of recommended movies
    and they key data based on users personal preference
    Returns:
        json: data is returned in json format.
    """
    response = jsonify({'value': 'not available'})
    if request.args['ratings'] != '':
        cookie_raw = request.args['ratings']
        cookie = json.loads(cookie_raw)
        ratings = helper.ratings_helper(cookie)
        if ratings is False:
            response = jsonify({'value': 'not available'})
        else:
            results = recommendations.get_movie_recommendations(ratings, 20)
            all_values = []
            for result in results:
                value = TableMovieTmdbDataFull.query \
                        .filter_by(movie_tmdb_data_full_movieid = result).first()
                all_values.append(value)

            allvalues_dict = helper.dict_helper(all_values)
            response = jsonify(allvalues_dict)
    else:
        response = jsonify({'value': 'not available'})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/dbgetmoviesbypersonalgenre", methods = ['GET'])
def db_get_movies_by_personal_genre():
    """
    This route implements a page that lists a limited number (20) of recommended
    movies and they key data based on users personal genre preference
    Returns:
        json: data is returned in json format.
    """
    response = jsonify({'value': 'not available'})
    if request.args['ratings'] != '':
        cookie_raw = request.args['ratings']
        cookie = json.loads(cookie_raw)
        ratings = helper.ratings_helper(cookie)

        if ratings is False:
            response = jsonify({'value': 'not available'})
        else:
            results = recommendations.get_movie_recommendations(ratings, 1)
            for result in results:
                value = TableMovieTmdbDataFull.query \
                    .filter_by(movie_tmdb_data_full_movieid = result).first()
            genre = helper.split_helper(value.movie_tmdb_data_full_genres)
            allvalues = TableMovieTmdbDataFull.query \
                        .filter(TableMovieTmdbDataFull.movie_tmdb_data_full_genres.ilike(genre)) \
                        .limit(20).all()
        allvalues_dict = helper.dict_helper(allvalues)
        response = jsonify(allvalues_dict)
    else:
        response = jsonify({'value': 'not available'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/dbgetpersonalrecommendations", methods = ['GET'])
def get_personal_recommendations():
    """
    This route implements a page that lists a limited number (20) of recommended
    movies and books and they key data based on users personal preference
    Returns:
        json: data is returned in json format.
    """
    response = jsonify({'value': 'not available'})
    if request.args['ratings'] != '':
        cookie_raw = request.args['ratings']
        cookie = json.loads(cookie_raw)
        ratings = helper.ratings_helper(cookie)
        if ratings is False:
            response = jsonify({'value': 'not available'})
        else:
            results = recommendations.get_all_recommendations(ratings, 20)
            movie_values = []
            for result in results["movies"]:
                value = TableMovieTmdbDataFull.query \
                        .filter_by(movie_tmdb_data_full_movieid = result).first()
                movie_values.append(value)

            movie_values_dict = helper.dict_helper(movie_values)

            book_values = []
            for result in results["books"]:
                value = TableBkMetadata.query \
                        .filter_by(bk_metadata_item_id = result).first()
                book_values.append(value)

            book_values_dict = helper.dict_helper(book_values)

            all_values_dict = {}
            all_values_dict["movies"] = movie_values_dict
            all_values_dict["books"] = book_values_dict

            response = jsonify(all_values_dict)
    else:
        response = jsonify({'value': 'not available'})

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
