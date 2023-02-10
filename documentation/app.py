import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

# Movie classes

class TableMvTags(db.Model):
    __tablename__ = 'mv_tags'
    mv_tags_tag = db.Column('tag', db.String(255), primary_key=True) #orm: must set one as primary key
    mv_tags_id = db.Column('id', db.Integer)

    def object_to_dictionary(self):
        return {
            'tag': self.mv_tags_tag,
            'id': self.mv_tags_id
            }

class TableMovieTmdbDataFull(db.Model):
    __tablename__ = 'movie_tmdb_data_full'
    movie_tmdb_data_full_movieid = db.Column('movieid', db.Integer, primary_key=True)
    movie_tmdb_data_full_tmdbmovieid = db.Column('tmdbmovieid', db.Integer)
    movie_tmdb_data_full_title = db.Column('title', db.String(251))
    movie_tmdb_data_full_originaltitle = db.Column('originaltitle', db.String(252))
    movie_tmdb_data_full_collection = db.Column('collection', db.String(253))
    movie_tmdb_data_full_genres = db.Column('genres', db.String(2001))
    movie_tmdb_data_full_actors = db.Column('actors', db.String(65535))
    movie_tmdb_data_full_directors = db.Column('directors', db.String(2002))
    movie_tmdb_data_full_posterpath = db.Column('posterpath', db.String(254))
    movie_tmdb_data_full_youtubetrailerids = db.Column('youtubetrailerids', db.String(1000))
    movie_tmdb_data_full_plotsummary = db.Column('plotsummary', db.String(65535))
    movie_tmdb_data_full_tagline = db.Column('tagline', db.String(2003))
    movie_tmdb_data_full_releasedate = db.Column('releasedate', db.Date)
    movie_tmdb_data_full_originallanguage = db.Column('originallanguage', db.String(100))
    movie_tmdb_data_full_languages = db.Column('languages', db.String(256))
    movie_tmdb_data_full_mpaa = db.Column('mpaa', db.String(100))
    movie_tmdb_data_full_runtime = db.Column('runtime', db.Integer)
    movie_tmdb_data_full_budget = db.Column('budget', db.BigInteger)
    movie_tmdb_data_full_revenue = db.Column('revenue', db.Integer) # oli: BigInteger
    movie_tmdb_data_full_lastupdated = db.Column('lastupdated', db.DateTime)
    movie_tmdb_data_full_backdroppaths = db.Column('backdroppaths', db.String(10000))

    def object_to_dictionary(self):
        return {
            'movieid': self.movie_tmdb_data_full_movieid,
            'tmdbmovieid': self.movie_tmdb_data_full_tmdbmovieid,
            'title': self.movie_tmdb_data_full_title,
            'originaltitle': self.movie_tmdb_data_full_originaltitle,
            'collection': self.movie_tmdb_data_full_collection,
            'genres': self.movie_tmdb_data_full_genres,
            'actors': self.movie_tmdb_data_full_actors,
            'directors': self.movie_tmdb_data_full_directors,
            'posterpath': self.movie_tmdb_data_full_posterpath,
            'youtubetrailerids': self.movie_tmdb_data_full_youtubetrailerids,
            'plotsummary': self.movie_tmdb_data_full_plotsummary,
            'releasedate': self.movie_tmdb_data_full_releasedate,
            'originallanguage': self.movie_tmdb_data_full_originallanguage,
            'languages': self.movie_tmdb_data_full_languages,
            'mpaa': self.movie_tmdb_data_full_mpaa,
            'runtime': self.movie_tmdb_data_full_runtime,
            'budget': self.movie_tmdb_data_full_budget,
            'revenue': self.movie_tmdb_data_full_revenue,
            'lastupdated': self.movie_tmdb_data_full_lastupdated,
            'backdroppaths': self.movie_tmdb_data_full_backdroppaths,
            }

class TableMvMetadataUpdated(db.Model):
    __tablename__ = 'mv_metadata_updated'
    mv_metadata_updated_title = db.Column('title', db.String(2001), primary_key=True)
    mv_metadata_updated_directedby = db.Column('directedby', db.String(2002))
    mv_metadata_updated_starring = db.Column('starring', db.String(2003))
    mv_metadata_updated_avgrating = db.Column('avgrating', db.Integer)
    mv_metadata_updated_imdbid = db.Column('imdbid', db.String(20))
    mv_metadata_updated_item_id = db.Column('item_id', db.Integer)

    def object_to_dictionary(self):
        return {
            'title': self.mv_metadata_updated_title,
            'directedby': self.mv_metadata_updated_directedby,
            'starring': self.mv_metadata_updated_starring,
            'avgrating': self.mv_metadata_updated_avgrating,
            'imdbid': self.mv_metadata_updated_imdbid,
            'item_id': self.mv_metadata_updated_item_id,
            }

# Input testing

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

# Book classes

class TableBkMetadata(db.Model):
    __tablename__ = 'bk_metadata'
    bk_metadata_item_id = db.Column('item_id', db.Integer, primary_key=True)
    bk_metadata_url = db.Column('url', db.String(1000))
    bk_metadata_title = db.Column('title', db.String(255))
    bk_metadata_authors = db.Column('authors', db.String(2000))
    bk_metadata_lang = db.Column('lang', db.String(255))
    bk_metadata_img = db.Column('img', db.String(1000))
    bk_metadata_year = db.Column('year', db.Integer)
    bk_metadata_description = db.Column('description', db.String(65535))

    def object_to_dictionary(self):
        return {
            'item_id': self.bk_metadata_item_id,
            'url': self.bk_metadata_url,
            'title': self.bk_metadata_title,
            'authors': self.bk_metadata_authors,
            'lang': self.bk_metadata_lang,
            'img': self.bk_metadata_img,
            'year': self.bk_metadata_year,
            'description': self.bk_metadata_description,
            }

def dict_helper(object_list):
    return [item.object_to_dictionary() for item in object_list]

@app.route('/')
def index():
    return 'Index page'

@app.route('/hello')
def hello():
    return 'Hello, World'

# Movie routes

@app.route('/dbgettags', methods = ['GET'])
def gettablevalues():
    allvalues = TableMvTags.query.all()
    allvalues_dict = dict_helper(allvalues)
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
    allvalues = TableMovieTmdbDataFull.query.filter_by(movie_tmdb_data_full_movieid = 6).first()
    response = jsonify(allvalues.object_to_dictionary())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgetgivenmoviedata', methods = ['GET'])
def get_given_movie_data():
    if request.args['movieid'] != '':
        if request.args['movieid'].isdigit():
            movieid = int(request.args['movieid'])
            allvalues = TableMovieTmdbDataFull.query.filter_by(movie_tmdb_data_full_movieid = movieid).first()
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
                        TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate) == year_value).order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_revenue.desc().nulls_last()).limit(10).all()
    allvalues_dict = dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10newestpublishedmovies', methods = ['GET'])
def get_top_10_newest_published_movies():
    date_value = date.today()
    allvalues = TableMovieTmdbDataFull.query.filter(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate<date_value).order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate.desc()).limit(10).all()
    allvalues_dict = dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10oldestmovies', methods = ['GET'])
def get_top_10_oldest_movies():
    allvalues = TableMovieTmdbDataFull.query.order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate.asc()).limit(10).all()
    allvalues_dict = dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbsearchmoviesbyname', methods = ['GET'])
def search_movies_by_name_top_20():
    search_raw = request.args['input']
    search_term = f'%{search_raw}%'
    allvalues = TableMovieTmdbDataFull.query.filter(TableMovieTmdbDataFull.movie_tmdb_data_full_title.ilike(search_term)).order_by(TableMovieTmdbDataFull.movie_tmdb_data_full_title.ilike(search_term).desc(), TableMovieTmdbDataFull.movie_tmdb_data_full_title).limit(20).all()
    allvalues_dict = dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/dbgettop10highestratedmovies', methods = ['GET'])
def get_top_10_highest_rating_movies():
    allvalues = db.session.query(TableMovieTmdbDataFull, TableMvMetadataUpdated) \
                          .join(TableMvMetadataUpdated, TableMvMetadataUpdated.mv_metadata_updated_item_id == TableMovieTmdbDataFull.movie_tmdb_data_full_movieid) \
                          .order_by(TableMvMetadataUpdated.mv_metadata_updated_avgrating.desc().nulls_last(), TableMovieTmdbDataFull.movie_tmdb_data_full_releasedate.desc().nulls_last()) \
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

# Book routes

@app.route('/dbgettop10newestbooks', methods = ['GET'])
def get_top_10_newest_books():
    allvalues = TableBkMetadata.query \
                .order_by(TableBkMetadata.bk_metadata_year.desc().nulls_last(), TableBkMetadata.bk_metadata_title.asc()) \
                .limit(10).all()
    allvalues_dict = dict_helper(allvalues)
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
    allvalues_dict = dict_helper(allvalues)
    response = jsonify(allvalues_dict)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
