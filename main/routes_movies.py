"""
This module implements routes for movies data in the flask app.
"""

from datetime import date
from flask import jsonify, request
from app import app
from main.extentions import db
from main.movies import TableMovieTmdbDataFull, TableMvMetadataUpdated, TableMvTags, TableMvSimilarMvbk
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
                    .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate.desc()) \
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

#@app.route('/dbsearchmoviesbynamen', methods = ['GET'])
#def search_movies_by_name_top_n():
#    """This route implements a page that shows data for a number of movies whose
#    name is closest to the search term typed by user. Number needs to defined;
#    it is has not been defined, a default value is returned.
#
#    Returns:
#        json: Data is returned in json format.
#    """
#    number_of_movies_default = 20
#    if request.args['amount'] != '':
#        if request.args['amount'].isdigit():
#            number_of_movies = request.args['amount']
#        else:
#            number_of_movies = number_of_movies_default
#    else:
##        number_of_movies = request.args.get('amount', 3)
#        number_of_movies = number_of_movies_default
#
#    search_raw = request.args['input']
#    search_term = f'%{search_raw}%'
#    allvalues = TableMovieTmdbDataFull.query \
#                    .filter(TableMovieTmdbDataFull.movie_tmdb_data_full_title.ilike(search_term)) \
#                    .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_title.ilike(search_term).desc(),
#                            TableMovieTmdbDataFull.movie_tmdb_data_full_title) \
#                    .limit(number_of_movies).all()
#    allvalues_dict = helper.dict_helper(allvalues)
#    response = jsonify(allvalues_dict)
#
#    response.headers.add('Access-Control-Allow-Origin', '*')
#    return response

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
        #print(value.TableMovieTmdbDataFull.movie_tmdb_data_full_movieid)
        #print(value.TableMovieTmdbDataFull.movie_tmdb_data_full_title)
        #print(value.TableMvMetadataUpdated.mv_metadata_updated_avgrating)

        #allvalues_dict.append({'movieid': value.TableMovieTmdbDataFull.movie_tmdb_data_full_movieid,
        # 'title': value.TableMovieTmdbDataFull.movie_tmdb_data_full_title,
        # 'avgrating': value.TableMvMetadataUpdated.mv_metadata_updated_avgrating})
        dict_1 = value.TableMovieTmdbDataFull.object_to_dictionary()
        dict_2 = value.TableMvMetadataUpdated.object_to_dictionary()
        dict_1.update(dict_2)
        allvalues_dict.append(dict_1)

    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetrecommendeditemsforgivenmovie', methods = ['GET'])
def get_recommended_items_for_given_movie():
    """This route implements a page that lists the recommended 10 movies for
    a given movie that needs to be defined when calling the route.
    """
    if request.args['movieid'] != '':
        if request.args['movieid'].isdigit():
            movieid = int(request.args['movieid'])
            ref_item_type = 'movie'
            allvalues = TableMvSimilarMvbk.query \
                            .filter_by( mv_similar_mvbk_item_id = movieid,
                                        mv_similar_mvbk_similar_item_type = ref_item_type) \
                            .order_by(TableMvSimilarMvbk.mv_similar_mvbk_similarity_score.desc()) \
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

@app.route('/dbgetrecommendationsalldataforgivenmovie', methods = ['GET'])
def get_recommendations_all_data_for_given_movie():
    """This route implements a page that lists the recommended 10 movies and their key data for
    a given movie that needs to be defined when calling the route

    Returns:
        json: data is returned in json format.
    """
#    movieid = 1
    ref_item_type = 'movie'
    if request.args['movieid'] != '':
        if request.args['movieid'].isdigit():
            movieid = int(request.args['movieid'])
            allvalues = db.session.query(TableMovieTmdbDataFull, TableMvSimilarMvbk) \
                            .join(TableMvSimilarMvbk, TableMvSimilarMvbk.mv_similar_mvbk_similar_item_id == TableMovieTmdbDataFull.movie_tmdb_data_full_movieid) \
                            .filter_by( mv_similar_mvbk_item_id = movieid,
                                        mv_similar_mvbk_similar_item_type = ref_item_type) \
                            .order_by(TableMvSimilarMvbk.mv_similar_mvbk_similarity_score.desc()) \
                            .offset(1) \
                            .all()
        #    print(len(allvalues))
            if len(allvalues) != 0:
                allvalues_dict = []
                for value in allvalues:
                    dict_1 = value.TableMovieTmdbDataFull.object_to_dictionary()
                    dict_2 = value.TableMvSimilarMvbk.object_to_dictionary()
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

@app.route("/dbgetpersonalmovierecommendations", methods = ['GET', "POST"])
def get_personal_movie_recommendations():
    cookie = request.get_json()
    if cookie:

        ratings = helper.ratings_helper(cookie)
        if ratings is False:
            response = jsonify({'value': 'not available'})
        else:

            results = recommendations.get_movie_recommendations(ratings, 10)

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
