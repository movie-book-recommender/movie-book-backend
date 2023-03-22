import pandas as pd

tg_movies = pd.read_csv("./movie_dataset_public_final/scores/tagdl.csv")
tg_books = pd.read_csv("./book_dataset/scores/tagdl.csv")

book_tags = set(tg_books.tag.unique())
movie_tags = set(tg_movies.tag.unique())
common_tags = book_tags.intersection(movie_tags)
book_ids = set(tg_books.item_id.unique())
movie_ids = set(tg_movies.item_id.unique())
#print(len(book_ids))
#print(len(movie_ids))

def get_vector_length(target_item):
    item_tmp = target_item.copy()
    item_tmp.score = item_tmp.score * item_tmp.score
    item_vector_len = item_tmp.score.sum()
    item_vector_len = item_vector_len**(1/2)
    return item_vector_len

def get_dot_product(target_item, tg_df):
    tg_domain_target_item = pd.merge(tg_df, target_item, on='tag', how='inner')
    tg_domain_target_item['dot_product'] = tg_domain_target_item.score_x * tg_domain_target_item.score_y
    dot_product_df = tg_domain_target_item.groupby('item_id_x').dot_product.sum().reset_index()
    return dot_product_df

def get_item_length_df(tg_df):
    len_df = tg_df.copy()
    len_df["length"] = len_df.score * len_df.score
    len_df = len_df.groupby("item_id")["length"].sum().reset_index()
    len_df["length"] = len_df["length"]**(1/2)
    return len_df

def get_sim_df(dot_product_df, len_df, profile_vector_len):
    sim_df = pd.merge(dot_product_df, len_df, left_on="item_id_x", right_on="item_id")
    sim_df["sim"] = sim_df["dot_product"] / sim_df["length"] / profile_vector_len
    return sim_df

full_dataframe = pd.DataFrame(columns=["i", "item_id", "item_type", "sim"])

for i in movie_ids:
    print(i)
    #if i == 21856269:
        #break
    target_movie = tg_movies[tg_movies.item_id == i].copy()

    target_movie_limited_len = get_vector_length(target_movie[target_movie.tag.isin(common_tags)])
    movie_to_books_dot_product = get_dot_product(target_movie[target_movie.tag.isin(common_tags)], tg_books)

    book_len_df = get_item_length_df(tg_books[tg_books.tag.isin(common_tags)])
    related_books_sim_df = get_sim_df(movie_to_books_dot_product, book_len_df, target_movie_limited_len)
    top250_books_related_to_movie = related_books_sim_df.sort_values("sim", ascending=False).head(250)

    result = related_books_sim_df.sort_values("sim", ascending=False, ignore_index=True).head(250).drop(columns=["dot_product", "length", "item_id_x"])
    result["i"] = i
    result["item_type"] = "book"
    #print(result)
    full_dataframe = full_dataframe.append(result)
    full_dataframe.to_csv("mv_to_bks_sim.csv", index=False)
