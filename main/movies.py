"""
This module outlines the contents of all the tables with data
regarding movies in the application's database.
"""

from main.extentions import db

class TableMvTags(db.Model):
    """This class outlines the structure of the MvTags table
    in the application's database, and the related methods.
    Note. Use of orm syntax requires setting one one of
    items as primary key, though it has not been defined in the
    underlying database.

    Args:
        db (object): Table shows tags for movies.

    Returns:
        Integer, string: Returns data as integers or strings.
    """
    __tablename__ = 'mv_tags'
    mv_tags_tag = db.Column('tag', db.String(255), primary_key=True)
    mv_tags_id = db.Column('id', db.Integer)

    def object_to_dictionary(self):
        """This method returns contents of the MvTags table
        in a dictionary format.

        Returns:
            Dictionary: Returns contents of the MvTags table.
        """
        return {
            'tag': self.mv_tags_tag,
            'id': self.mv_tags_id
            }

class TableMovieTmdbDataFull(db.Model):
    """This class outlines the structure of the MovieTMDBDataFull table
    in the application's database, and the related methods.

    Args:
        db (object): Table shows data related to movies.

    Returns:
        Integer, string, date, datetime: Returns table's data as e.g., integers.
    """
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
    movie_tmdb_data_full_revenue = db.Column('revenue', db.Integer)
    movie_tmdb_data_full_lastupdated = db.Column('lastupdated', db.DateTime)
    movie_tmdb_data_full_backdroppaths = db.Column('backdroppaths', db.String(10000))

    def object_to_dictionary(self):
        """This method returns contents of the MovieTmdbDataFull table
        in a dictionary format.

        Returns:
            Dictionary: Returns contents of the MovieTmdbDataFull table.
        """
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
    """This class outlines the structure of the MvMetadataUpdated table
    in the application's database, and the related methods.

    Args:
        db (object): Tables contains updated metadata for movies.

    Returns:
        Integer, string: Returns data from table as integers or strings.
    """
    __tablename__ = 'mv_metadata_updated'
    mv_metadata_updated_title = db.Column('title', db.String(2001), primary_key=True)
    mv_metadata_updated_directedby = db.Column('directedby', db.String(2002))
    mv_metadata_updated_starring = db.Column('starring', db.String(2003))
    mv_metadata_updated_avgrating = db.Column('avgrating', db.Integer)
    mv_metadata_updated_imdbid = db.Column('imdbid', db.String(20))
    mv_metadata_updated_item_id = db.Column('item_id', db.Integer)

    def object_to_dictionary(self):
        """This method returns contents of the MvMetadataUpdated table
        in a dictionary format.

        Returns:
            Dictionary: Returns contents of the MvMetadataUpdated table.
        """
        return {
            'title': self.mv_metadata_updated_title,
            'directedby': self.mv_metadata_updated_directedby,
            'starring': self.mv_metadata_updated_starring,
            'avgrating': self.mv_metadata_updated_avgrating,
            'imdbid': self.mv_metadata_updated_imdbid,
            'item_id': self.mv_metadata_updated_item_id,
            }

class TableMvSimilarMovies(db.Model):
    """This class outlines the structure of the MvSimilarMovies table
    in the application's database, and the related methods.

    Args:
        db (object): Table contains for each movie the top 251 movies
        that are most similar to this movie.

    Returns:
        Integer, string: Returns data from table as integers or strings.
    """
    __tablename__ = 'mv_similar_movies'
    mv_similar_movies_item_id = db.Column('item_id', db.Integer)
    mv_similar_movies_similar_item_id = db.Column('similar_item_id', db.Integer)
    mv_similar_movies_similar_item_type = db.Column('similar_item_type', db.String(16))
    mv_similar_movies_similarity_score = db.Column('similarity_score', db.Integer)
    mv_similar_movies_row_index = db.Column('row_index', db.Integer, primary_key=True)

    def object_to_dictionary(self):
        """This method returns contents of the MvSimilarMovies table
        in a dictionary format.

        Returns:
            Dictionary: Returns contents of the MvSimilarMovies table.
        """
        return {
            'item_id': self.mv_similar_movies_item_id,
            'similar_item_id': self.mv_similar_movies_similar_item_id,
            'similar_item_type': self.mv_similar_movies_similar_item_type,
            'similarity_score': self.mv_similar_movies_similarity_score,
            'row_index': self.mv_similar_movies_row_index
            }

class TableMvSimilarBooks(db.Model):
    """This class outlines the structure of the MvSimilarBooks table
    in the application's database, and the related methods.

    Args:
        db (object): Table contains for each movie the top 250 books
        that are most similar to this movie.

    Returns:
        Integer, string: Returns data from table as integers or strings.
    """
    __tablename__ = 'mv_similar_books'
    mv_similar_books_item_id = db.Column('item_id', db.Integer)
    mv_similar_books_similar_item_id = db.Column('similar_item_id', db.Integer)
    mv_similar_books_similar_item_type = db.Column('similar_item_type', db.String(16))
    mv_similar_books_similarity_score = db.Column('similarity_score', db.Integer)
    mv_similar_books_row_index = db.Column('row_index', db.Integer, primary_key=True)

    def object_to_dictionary(self):
        """This method returns contents of the MvSimilarBooks table
        in a dictionary format.

        Returns:
            Dictionary: Returns contents of the MvSimilarBooks table.
        """
        return {
            'item_id': self.mv_similar_books_item_id,
            'similar_item_id': self.mv_similar_books_similar_item_id,
            'similar_item_type': self.mv_similar_books_similar_item_type,
            'similarity_score': self.mv_similar_books_similarity_score,
            'row_index': self.mv_similar_books_row_index
            }

class TableMvTagDl(db.Model):
    """This class outlines the structure of the MvTagDl table
    in the application's database, and the related methods.
    Note. Use of orm syntax requires setting one one of
    items as primary key, though it has not been defined in the
    underlying database.

    Args:
        db (object): Table shows tags for movies.

    Returns:
        Integer, string: Returns data as integers or strings.
    """
    __tablename__ = 'mv_tagdl'
    mv_tagdl_tag = db.Column('tag', db.String(255), primary_key=True)
    mv_tagdl_item_id = db.Column('item_id', db.Integer)
    mv_tagdl_score = db.Column("score", db.Integer, primary_key=True)
    mv_tagdl_row_index = db.Column('row_index', db.Integer, primary_key=True)

    def object_to_dictionary(self):
        """This method returns contents of the MvTagDl table
        in a dictionary format.

        Returns:
            Dictionary: Returns contents of the MvTagDl table.
        """
        return {
            'tag': self.mv_tagdl_tag,
            'item_id': self.mv_tagdl_item_id,
            "score": self.mv_tagdl_score,
            "row_index": self.mv_tagdl_row_index
            }
