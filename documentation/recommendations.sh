# These commands calculate recommendations between movies and movies, books and books, movies and books and books and movies and add them to the database.
python3 mv_to_mvs.py
psql -U moviebook -d mvbkdb -c "\copy mv_similar_movies (item_id, similar_item_id, similar_item_type, similarity_score) FROM 'mv_to_mvs_updated.csv' delimiter ',' csv header"
python3 book_to_books.py
psql -U moviebook -d mvbkdb -c "\copy bk_similar_books (item_id, similar_item_id, similar_item_type, similarity_score) FROM 'bk_to_bks_updated.csv' delimiter ',' csv header"
python3 movie_to_books.py
psql -U moviebook -d mvbkdb -c "\copy mv_similar_books (item_id, similar_item_id, similar_item_type, similarity_score) FROM 'mv_to_bks_sim.csv' delimiter ',' csv header"
python3 book_to_movies.py
psql -U moviebook -d mvbkdb -c "\copy bk_similar_movies (item_id, similar_item_id, similar_item_type, similarity_score) FROM 'bk_to_mvs.csv' delimiter ',' csv header"
