"""
This module implements methods to get the data and 
to calculate recommendations based on user's preferences.
"""

import os
from os import getenv
#import time
import pandas as pd

class Recommendations:
    """Class that generates personal recommendations for users.
       Main functions are get_movie_recommendations and
       get_book_recommendations.
    """
    def __init__(self):
        """Initializes tag resources from database.
        """
        self.data_uploaded = False
        pass

    def get_data(self):
        """ Method opens and reads files containing data for movies' and 
            books' tags if the application is not run on GitHub.
            Note. Data used contains tag files that are limited to tags
            where the score is above 0.1.
        """
        print("is in getting data function")
        if os.getenv("ACTIONS_CI") != "is_in_github":
            print("... and is not github action")
            self.tg_movies = pd.read_csv("./datasets/movies_tagdl_common_limited.csv")
            self.tg_books = pd.read_csv("./datasets/books_tagdl_common_limited.csv")

            self.data_uploaded = True

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
            weight = rating["rating"] - 2.5
            item = tg[tg.item_id == rating["item_id"]].copy()
            item.score = item.score * weight
            df = pd.concat([df, item])

        return df

    def get_dot_product(self, profile, tg_df):
        """Generates dot product for all items

        Args:
            profile (Dataframe): Created user profile that was created in get_user_profile.
            tg_df (Dataframe): Tag Dataframe

        Returns:
            Dataframe: Dataframe that has the item_id_x and the dot products
        """

        tg_domain_profile = pd.merge(tg_df, profile, on="tag_id", how="inner")

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
        """Main function to fetch recommendations for movies based on ratings.

        Args:
            ratings (dict): Dictionary that has fields movies and books
                            that have the ratings as id and value
            amount (int): The amount of results

        Returns:
            list: List of id's, which are the recommended movies
                  for the user. Best one is at index 0.
        """
        if self.data_uploaded == False:
            print("data is not yet uploaded")
            self.get_data()
        else:
            print("data is already uploaded")

        profile = self.get_user_profile(self.tg_movies, ratings["movies"])

        profile = pd.concat([profile, self.get_user_profile(self.tg_books, ratings["books"])])

        movie_dot_product = self.get_dot_product(profile, self.tg_movies)

        movie_len_df = self.get_item_length_df(self.tg_movies)

        profile_vector_len = self.get_vector_length(profile)

        movie_sim_df = self.get_sim_df(movie_dot_product, movie_len_df, profile_vector_len)

        results = movie_sim_df.sort_values("sim", ascending=False, ignore_index=True).head(amount).drop(columns=["dot_product", "length", "item_id_x", "sim"])

        results = results["item_id"].values.tolist()

        return results

    def get_book_recommendations(self, ratings, amount):
        """
        Main function to fetch recommendations for books based on ratings.
        Args:
            ratings (dict): Dictionary that has fields movies and 
                            books that have the ratings as id and value
            amount (int): The amount of results
        Returns:
            list: List of id's, which are the recommended movies for 
                  the user. Best one is at index 0.
        """
        if self.data_uploaded == False:
            print("data is not yet uploaded")
            self.get_data()
        else:
            print("data is already uploaded")

        profile = self.get_user_profile(self.tg_books, ratings["books"])

        profile = pd.concat([profile, self.get_user_profile(self.tg_movies, ratings["movies"])])

        book_dot_product = self.get_dot_product(profile, self.tg_books)

        book_len_df = self.get_item_length_df(self.tg_books)

        profile_vector_len = self.get_vector_length(profile)

        book_sim_df = self.get_sim_df(book_dot_product, book_len_df, profile_vector_len)

        results = book_sim_df.sort_values("sim", ascending=False, ignore_index=True).head(amount).drop(columns=["dot_product", "length", "item_id_x", "sim"])

        results = results["item_id"].values.tolist()

        return results

    def get_all_recommendations(self, ratings, amount):
        """Function to fetch both movie and book recommendations

        Args:
            ratings (dict): Dictionary that has fields movies and books
                            that have the ratings as id and value
            amount (int): The amount of results wanted
        Returns:
            dict: Dictionary that has keys "movies" and "books" 
            which includes corresponding lists of recommended item ID's.
        """

        results = {}
        results["movies"] = self.get_movie_recommendations(ratings, amount)
        results["books"] = self.get_book_recommendations(ratings, amount)

        return results


recommendations = Recommendations()

# Ratings should look like this:

#ratings = {"movies" : [{"item_id" : 1270, "rating" : 4}, # Back to the Future
#                       {"item_id" : 5445, "rating" : 5}, # Minority Report
#                       {"item_id" : 7361, "rating" : 1}], # Eternal Sunshine of the Spotless Mind
#           "books" : [{"item_id" : 150259, "rating" : 4}, # Stephen King - IT
#                      {"item_id" : 3230869, "rating" : 3}]} # Stephen King -Misery
#
#
##example:
#print(recommendations.get_movie_recommendations(ratings, 11))

# Result: [5445 minority report, 1240 terminator, 589 terminator 2, 68358 star trek, 1270 back to the future, 2571 the matrix, 1036 die hard, 6537 terminator 3, 85414, 8644 i, robot, 2916 total recall]
