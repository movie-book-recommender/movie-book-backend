# These commands calculate recommendations between movies and movies, books and books, movies and books and books and movies and add them to the database.
python3 mv_to_mvs.py
psql -U moviebook -d mvbkdb -c "\copy mv_similar_movies (item_id, similar_item_id, similar_item_type, similarity_score) FROM 'mv_to_mvs_updated.csv' delimiter ',' csv header"
python3 book_to_books.py
psql -U moviebook -d mvbkdb -c "\copy bk_similar_books (item_id, similar_item_id, similar_item_type, similarity_score) FROM 'bk_to_bks_updated.csv' delimiter ',' csv header"
python3 movie_to_books.py
psql -U moviebook -d mvbkdb -c "\copy mv_similar_books (item_id, similar_item_id, similar_item_type, similarity_score) FROM 'mv_to_bks_sim.csv' delimiter ',' csv header"
python3 book_to_movies.py
psql -U moviebook -d mvbkdb -c "\copy bk_similar_movies (item_id, similar_item_id, similar_item_type, similarity_score) FROM 'bk_to_mvs.csv' delimiter ',' csv header"

# These commands calculate optimized tag files used as a basis for user generated recommendations.
python3 common_tags.py
sed 's/\r//' common_tags.csv > common_tags2.csv
psql -U moviebook -d mvbkdb -c "\copy common_tags (common_tag, common_tag_id) FROM 'common_tags2.csv' delimiter ',' csv header"
python3 movies_tagdl_common.py
psql -U moviebook -d mvbkdb -c "\copy mv_tagdl_common (item_id, score, common_tag_id) FROM 'movies_tagdl_common_all.csv' delimiter ',' csv header"
python3 books_tagdl_common.py
psql -U moviebook -d mvbkdb -c "\copy bk_tagdl_common (item_id, score, common_tag_id) FROM 'books_tagdl_common_all.csv' delimiter ',' csv header"
python3 mvs_bks_tagdl_common_limited.py