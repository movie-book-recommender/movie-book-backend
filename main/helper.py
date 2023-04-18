"""
This module implement general methods used across all classes.
"""

class Helper:
    """
    This class implements methods used across all other classes.
    """
    def __init__(self):
        pass

    def dict_helper(self, object_list):
        """
        This method implements conversion of input into a dictionary

        Args:
            object_list (list): List of objects.

        Returns:
            Dictionary: Returns the given data in dictionary form.
        """
        return [item.object_to_dictionary() for item in object_list]

    def ratings_helper(self, cookie):
        """Helper function between the cookie from the frontend and 
        the recommendation algorithm in the backend to parse the cookie 
        in a form that is easier to handle when forming recommendations.

        Args:
            cookie (JSON): JSON including ratings, looks something
            like this: {"Books":[["52951446","1"],["45424741","4"],
            ["1168090","5"],["43166999","1"],["860196","5"]],
            "Movies":[["210579","1"],["3271","1"],["949","4"],
            ["1938","1"],["3475","5"]]}

        Returns:
            dict: Dictionary including keys "movies" and "books" and
            values are their relative ratings as lists.
        """
        if "Movies" not in cookie:
            ratings = False
        elif "Books" not in cookie:
            ratings = False
        elif len(cookie["Movies"]) == 0 and len(cookie["Books"]) == 0:
            ratings = False
        else:
            ratings = {"movies": [],
                    "books": []}
            movies = cookie["Movies"]
            if len(movies) != 0:
                for movie in movies:
                    if len(movie) < 2:
                        continue
                    else:
                        ratings["movies"].append({"item_id": int(movie[0]), "rating": int(movie[1])})
            books = cookie["Books"]
            if len(books) != 0:
                for book in books:
                    if len(book) < 2:
                        continue
                    else:
                        ratings["books"].append({"item_id": int(book[0]), "rating": int(book[1])})
        return ratings

    def split_helper(self, string):
        """Method returns first string in genres.

        Args:
            string (string): string consisting of movie's genres

        Returns:
            string: String consisting of movie's first genre. 
        """

        string_list = string.split(",", 1)
        result = string_list[0]
        return result

helper = Helper()
