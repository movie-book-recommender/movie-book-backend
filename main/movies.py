from main.extentions import db

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
