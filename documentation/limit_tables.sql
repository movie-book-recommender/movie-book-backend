/* These commands limit the data in the relevant tables for movies to the ones with tags
in movies_tagdl, which containts 9734 movies*/

/* Entries in movie_tmdb_data_full are limited to movies with tags available */
/* Number of movies was limited from 102690 movies to 9722 movies */

SELECT A.*
INTO public.movie_tmdb_data_full_temp
FROM public.movie_tmdb_data_full as A
INNER JOIN (
	SELECT DISTINCT item_id FROM public.mv_tagdl
) as B
ON A.movieid = B.item_id;

ALTER TABLE movie_tmdb_data_full
RENAME TO movie_tmdb_data_full_all;

ALTER TABLE movie_tmdb_data_full_temp
RENAME TO movie_tmdb_data_full;

/* Entries in mv_metadata are limited to movies with tags available */
/* Number of movies was limited from 84661 movies to 9730 movies */

SELECT A.*
INTO public.mv_metadata_temp
FROM public.mv_metadata as A
INNER JOIN (
	SELECT DISTINCT item_id FROM public.mv_tagdl
) as B
ON A.item_id = B.item_id;

ALTER TABLE mv_metadata
RENAME TO mv_metadata_all;

ALTER TABLE mv_metadata_temp
RENAME TO mv_metadata; 

/* Entries in mv_metadata_updated are limited to movies with tags available */
/* Number of movies was limited from 84661 movies to 9730 movies */

SELECT A.*
INTO public.mv_metadata_updated_temp
FROM public.mv_metadata_updated as A
INNER JOIN (
	SELECT DISTINCT item_id FROM public.mv_tagdl
) as B
ON A.item_id = B.item_id;

ALTER TABLE mv_metadata_updated
RENAME TO mv_metadata_updated_all;

ALTER TABLE mv_metadata_updated_temp
RENAME TO mv_metadata_updated;

/* Entries in mv_ratings are limited to movies with tags available */
/* Number of movies was limited from 67873 movies to 9734 movies */

SELECT A.*
INTO public.mv_ratings_temp
FROM public.mv_ratings as A
INNER JOIN (
	SELECT DISTINCT item_id FROM public.mv_tagdl
) as B
ON A.item_id = B.item_id;

ALTER TABLE mv_ratings
RENAME TO mv_ratings_all;

ALTER TABLE mv_ratings_temp
RENAME TO mv_ratings; 
