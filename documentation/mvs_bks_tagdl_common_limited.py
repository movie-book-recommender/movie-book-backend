# This script generates files with movies and books tags files that 
# (1) only have common tags and (2) whose score is above a minimum level.

import pandas as pd
import csv

minimum_score = 0.1

# Generate limited set of movies
df_movies_tagdl_common_all = pd.read_csv("movies_tagdl_common_all.csv")
print(df_movies_tagdl_common_all)
#number_of_rows = len(df_tg_movies_limited)
#print(number_of_rows)
#print(f"number of lines in the file: {len(tg_movies_limited)}")

temp_df = pd.DataFrame(df_movies_tagdl_common_all, columns=["item_id", "score", "tag_id"])

df_movies_tagdl_common_limited = temp_df[temp_df['score']>minimum_score]
print(df_movies_tagdl_common_limited)

df_movies_tagdl_common_limited.to_csv("movies_tagdl_common_limited.csv", index=False)


# Generate limited set of books tags
df_books_tagdl_common_all = pd.read_csv("books_tagdl_common_all.csv")
print(df_books_tagdl_common_all)
#number_of_rows = len(df_tg_movies_limited)
#print(number_of_rows)
#print(f"number of lines in the file: {len(tg_movies_limited)}")

temp_df_2 = pd.DataFrame(df_books_tagdl_common_all, columns=["item_id", "score", "common_tag_id"])

df_books_tagdl_common_limited= temp_df_2[temp_df_2['score']>minimum_score]
print(df_books_tagdl_common_limited)

df_books_tagdl_common_limited.to_csv("books_tagdl_common_limited.csv", index=False)
