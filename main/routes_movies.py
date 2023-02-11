from app import app
from main.extentions import db
from main.movies import TableMovieTmdbDataFull, TableMvMetadataUpdated, TableMvTags
from main.helper import Helper
from flask import jsonify, request
from datetime import date

@app.route('/dbgettags', methods = ['GET'])
def gettablevalues():
    allvalues = TableMvTags.query.all()
    allvalues_dict = Helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetonemoviedata', methods = ['GET'])
def get_one_movie_data():
    allvalues = TableMovieTmdbDataFull.query.first()
    response = jsonify(allvalues.object_to_dictionary())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetgivenmoviedata_test', methods = ['GET'])
def get_given_movie_data_test():
    allvalues = TableMovieTmdbDataFull.query \
                .filter_by(movie_tmdb_data_full_movieid = 6).first()
    response = jsonify(allvalues.object_to_dictionary())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetgivenmoviedata', methods = ['GET'])
def get_given_movie_data():
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
    year_value = int(request.args['year'])
    allvalues = TableMovieTmdbDataFull.query.filter(db.extract('year', 
                        TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate) == year_value) \
                        .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_revenue.desc().nulls_last()).limit(10).all()
    allvalues_dict = Helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10newestpublishedmovies', methods = ['GET'])
def get_top_10_newest_published_movies():
    date_value = date.today()
    allvalues = TableMovieTmdbDataFull.query \
                    .filter(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate<date_value) \
                    .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate.desc()) \
                    .limit(10).all()
    allvalues_dict = Helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10oldestmovies', methods = ['GET'])
def get_top_10_oldest_movies():
    allvalues = TableMovieTmdbDataFull.query \
                    .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate.asc()) \
                    .limit(10).all()
    allvalues_dict = Helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbsearchmoviesbyname', methods = ['GET'])
def search_movies_by_name_top_20():
    search_raw = request.args['input']
    search_term = f'%{search_raw}%'
    allvalues = TableMovieTmdbDataFull.query \
                    .filter(TableMovieTmdbDataFull.movie_tmdb_data_full_title.ilike(search_term)) \
                    .order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_title.ilike(search_term).desc(),
                    TableMovieTmdbDataFull.movie_tmdb_data_full_title) \
                    .limit(20).all()
    allvalues_dict = Helper.dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10highestratedmovies', methods = ['GET'])
def get_top_10_highest_rating_movies():
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
        #                       'title': value.TableMovieTmdbDataFull.movie_tmdb_data_full_title,
        #                       'avgrating': value.TableMvMetadataUpdated.mv_metadata_updated_avgrating})
        dict_1 = value.TableMovieTmdbDataFull.object_to_dictionary()
        dict_2 = value.TableMvMetadataUpdated.object_to_dictionary()
        dict_1.update(dict_2)
        allvalues_dict.append(dict_1)

    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
