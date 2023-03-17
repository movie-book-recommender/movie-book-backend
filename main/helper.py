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
        if "Movies" not in cookie:
            ratings = False
        elif "Books" not in cookie:
            ratings = False
        elif len(cookie["Movies"]) == 0 or len(cookie["Books"]) == 0:
            ratings = False
        else:
            ratings = {"movies": [],
                    "books": []}
            movies = cookie["Movies"]

            for movie in movies:
                if len(movie) < 2:
                    continue
                else:
                    ratings["movies"].append({"item_id": int(movie[0]), "rating": int(movie[1])})
            books = cookie["Books"]
            for book in books:
                if len(book) < 2:
                    continue
                else:
                    ratings["books"].append({"item_id": int(book[0]), "rating": int(book[1])})
        return ratings
helper = Helper()

#Cookie looks like this: {'Books': [], 'Movies': [['210579', '5'], ['270352', '1']]}

#cookie = {"movies": [[0,4], [1,3]],
#          "books": [[0,4], [1,3]]}

#print(helper.ratings_helper(cookie))