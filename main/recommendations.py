import pandas as pd
from main.movies import TableMvTagDl
from main.helper import helper
from flask import jsonify
from app import app

class Recommendations:
    """Class that generates personal recommendations for users. Main fucntion is get_movie_recommendations.
    """
    def __init__(self):
        """Initializes tag resources from database.
        """
        pass
        #self.tg_movies = pd.read_csv("/home/evahteri/Koulu/OHTUPROJEKTI/se_project/tagdl_movies.csv")
        #self.tg_movies = self.get_movie_tags()
        #self.tg_books = pd.read_csv("/home/evahteri/Koulu/OHTUPROJEKTI/se_project/tagdl_books.csv")
        #self.book_tags = set(self.tg_books.tag.unique()) # not needed during algo
        #self.movie_tags = set(self.tg_movies.tag.unique()) # not needed during algo
        #self.common_tags = self.book_tags.intersection(self.movie_tags) # this will be made as a single table
    

    def get_movie_tags(self):
        allvalues = TableMvTagDl.query.all()
        allvalues_dict = helper.dict_helper(allvalues)
        response = pd.DataFrame(allvalues_dict)
        return response

    def get_user_profile(self, tg, domain_ratings):
        """Generates a dataframe that represents user's preferences.

        Args:
            tg (dataframe): Dataframe that includes common tags.
            domain_ratings (dict): includes ratings made by user.

        Returns:
            Dataframe: Dataframe that includes the vector for the user.
        """
        df = pd.DataFrame()
        for rating in domain_ratings:
            weight = rating["rating"] - 2.5 # this is the weight of each rating
            item = tg[tg.item_id == rating["item_id"]].copy()
            item.score = item.score * weight # we multiply item vector by the weight based on the rating
            df = pd.concat([df, item]) # we add the item vector to the dataframe
        return df
    
    def get_dot_product(self, profile, tg_df):
        """Generates dot product for all items

        Args:
            profile (Dataframe): Created user profile that was created in get_user_profile.
            tg_df (Dataframe): Tag Dataframe

        Returns:
            Dataframe: Dataframe that has the item_id_x and the dot products
        """
        tg_domain_profile = pd.merge(tg_df, profile, on="tag", how="inner")
        tg_domain_profile["dot_product"] = tg_domain_profile.score_x * tg_domain_profile.score_y
        dot_product_df = tg_domain_profile.groupby("item_id_x").dot_product.sum().reset_index()

        # Returns:
        #        item_id_x  dot_product
        #        0             1   108.268884
        #        1             2    91.426635
        #        2             3    46.174985
        #        3             4    33.244906
        #        4             5    43.244255
        #        ...         ...          ...
        #        9729     106920   100.405217
        #        9730     107069    71.599322
        #        9731     107141    59.462259
        #        9732     107348    52.140476
        #        9733     108932    91.859114

        return dot_product_df
    
    def get_item_length_df(self, tg_df):
        """Calculates length for each movie

        Args:
            tg_df (Dataframe): The tag dataframe

        Returns:
            Dataframe: Dataframe that includes item_id and length
        """
        len_df = tg_df.copy()
        len_df["length"] = len_df.score * len_df.score
        len_df = len_df.groupby("item_id")["length"].sum().reset_index()
        len_df["length"] = len_df["length"]**(1/2)

        # Returns
        #    item_id    length
        #0        1  6.404624
        #1        2  5.729404
        #2        3  3.841003
        #3        4  3.794552
        #4        5  3.784929

        return len_df
    
    def get_vector_length(self, profile):
        """Calculates the vector length for the user

        Args:
            profile (dataframe): Dataframe with user data

        Returns:
            float: The calculated vector length.
        """
        prof_tmp = profile.copy()
        prof_tmp.score = prof_tmp.score * prof_tmp.score
        profile_vector_len = prof_tmp.score.sum()
        profile_vector_len = profile_vector_len**(1/2)

        # Returns:
        # 26.098431988201902

        return profile_vector_len
    
    def get_sim_df(self, dot_product_df, len_df, profile_vector_len):
        """Generates similarities for movies/books based on user profile

        Args:
            dot_product_df (dataframe)
            len_df (dataframe)
            profile_vector_len (float)

        Returns:
            Dataframe: Dataframe that has  the similarities for each item
        """
        sim_df = pd.merge(dot_product_df, len_df, left_on="item_id_x", right_on="item_id")
        sim_df["sim"] = sim_df["dot_product"] / sim_df["length"] / profile_vector_len


        return sim_df

    def get_movie_recommendations(self, ratings, amount):
        """Main function to fetch recommendations based on ratings.

        Args:
            ratings (dict): Dictionary that has fields movies and books that have the ratings as id and value
            amount (int): The amount of results

        Returns:
            list: List of id's, which are the recommended movies for the user. Best one is at index 0.
        """

        self.tg_movies = pd.read_csv("./movie_dataset_public_final/scores/tagdl.csv")
        #self.tg_movies_own = self.get_movie_tags()
        self.tg_books = pd.read_csv("./book_dataset/scores/tagdl.csv")
        self.book_tags = set(self.tg_books.tag.unique()) # not needed during algo
        self.movie_tags = set(self.tg_movies.tag.unique()) # not needed during algo
        self.common_tags = self.book_tags.intersection(self.movie_tags)

        print(self.tg_movies)
        print(self.tg_movies_own)


        profile = self.get_user_profile(self.tg_movies, ratings["movies"])
        profile = pd.concat([profile, self.get_user_profile(self.tg_books, ratings["books"])])

        movie_dot_product = self.get_dot_product(profile[profile.tag.isin(self.common_tags)], self.tg_movies) # we only consider common tags

        movie_len_df = self.get_item_length_df(self.tg_movies[self.tg_movies.tag.isin(self.common_tags)])

        profile_vector_len = self.get_vector_length(profile[profile.tag.isin(self.common_tags)])

        movie_sim_df = self.get_sim_df(movie_dot_product, movie_len_df, profile_vector_len)
        results = movie_sim_df.sort_values("sim", ascending=False, ignore_index=True).head(amount).drop(columns=["dot_product", "length", "item_id_x", "sim"])

        results = results["item_id"].values.tolist()

        #test_tags = self.get_movie_tags()
        #print(test_tags)

        return results

recommendations = Recommendations()
# example:
#print(recommendations.get_movie_recommendations(ratings, 11))