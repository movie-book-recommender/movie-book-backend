# This script identifies common tags between movies_tagdl.csv and books_tagdl.csv, gives a number for them and inserts into a csv file.

import pandas as pd
import csv

# Open files
#tg_movies = pd.read_csv("movies_tagdl.csv")
tg_movies = pd.read_csv("./movie_dataset_public_final/scores/tagdl.csv")
print(f"Number of rows in movies tags: {len(tg_movies)}")
#tg_books = pd.read_csv("books_tagdl.csv")
tg_books = pd.read_csv("./book_dataset/scores/tagdl.csv")
print(f"Number of rows in books tags: {len(tg_books)}")
#movie_ids = set(tg_movies.item_id.unique())
#print(movie_ids)

# Generate unique common tags
movie_tags = set(tg_movies.tag.unique())
print(f"Number of unique movie tags: {len(movie_tags)}")
book_tags = set(tg_books.tag.unique())
print(f"Number of unique book tags: {len(book_tags)}")
common_tags = book_tags.intersection(movie_tags)
print(f"Number of unique common tags: {len(common_tags)}")
print(common_tags)

sorted_common_tags=sorted(common_tags)
print(sorted_common_tags)

# Give each tag an identifier
common_tags_dict = {}
i = 1
for tag in sorted_common_tags: 
    common_tags_dict[tag] = i
    i += 1
print(f"Check: number of tags in the dictionary: {len(common_tags_dict)}")
print(common_tags_dict)

# Write tags into a file
with open('common_tags.csv', 'w', newline='') as common_tag_file:
    new_rows = csv.writer(common_tag_file)
    header_row = ["common_tag", "common_tag_id"]
    new_rows.writerow(header_row)
    for key in common_tags_dict.keys():
        common_tag_file.write("%s,%s\n"%(key,common_tags_dict[key]))
    common_tag_file.close()
