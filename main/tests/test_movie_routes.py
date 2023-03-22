import json
import unittest
from app import app

class TestMovieRoutes(unittest.TestCase):
    """This class implements tests for routes related to movies.

    Args:
        unittest (object): TBA
    """
    def setUp(self):
        """This is a test client that can handle get and post requests
        to test the APIs.
        """
        self.test_client = app.test_client()

    def test_get_given_movie_data(self):
        """Tests given movie data with id 210685 which is a movie called Trailer Made
        """
        response = self.test_client.get(
            "/dbgetgivenmoviedata?movieid=210685",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["title"], "Trailer Made")

    def test_get_top_10_movies_by_year(self):
        """Tests top ten movies by year, by checking if the first one is correct.
        """
        response = self.test_client.get(
            "/dbgettop10moviesbyyear?year=2020",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response[0]["title"],
                        "Demon Slayer -Kimetsu no Yaiba- The Movie: Mugen Train")

    def test_get_top_10_newest_published_movies(self):
        """Tests top ten newest published movies
        """
        response = self.test_client.get(
            "/dbgettop10newestpublishedmovies",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response[0]["title"], "Dead Men In The Skitrack")

    def test_search_movies_by_name_top_20(self):
        """Tests the search function. The first result with harry potter should be
        Harry Potter 20th Anniversary: Return to Hogwarts
        """
        response = self.test_client.get(
            "/dbsearchmoviesbyname?input=harry potter",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response[0]["title"],
                        "Harry Potter 20th Anniversary: Return to Hogwarts")

    def test_get_top_10_highest_rating_movies(self):
        """Tests the top 10 highest rated movies. The first one should be Assassins (2020)
        """
        response = self.test_client.get("/dbgettop10highestratedmovies",)
        json_response = json.loads(response.text)

        self.assertEqual((json_response[0]["title"], json_response[1]["title"],
                          json_response[2]["title"]), ("Assassins (2020)",
                          "There Will Be No More Night (2020)", "Halley's Comet (2020)"))

    def test_get_recommended_items_for_given_movie(self): # POISTA TÄMÄ TESTI
        """Tests whether 10 recommended movies are returned for a given movie.
        """
        response = self.test_client.get(
            "/dbgetrecommendeditemsforgivenmovie?movieid=5445",
        )
        json_response = json.loads(response.text)

        self.assertEqual(len(json_response), 10)

    def test_get_recommended_items_for_given_movie_wrong_input(self): # POISTA TÄMÄ TESTI
        """Tests whether correct error message is returned, if input is incorrect.
        """
        response = self.test_client.get(
            "/dbgetrecommendeditemsforgivenmovie?movieid=sdlkfjslfjlskjf",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")

    def test_get_for_given_movie_recommended_movies(self): # PÄIVITETTY TESTI
        """Tests whether 250 recommended movies are returned for a given movie.
        """
        response = self.test_client.get(
            "/dbgetforgivenmovierecommendedmovies?movieid=5445",
        )
        json_response = json.loads(response.text)
        wanted_answer = 250
        self.assertEqual(len(json_response), wanted_answer)

    def test_get_for_given_movie_recommended_movies_wrong_input(self): # PÄIVITETTY TESTI
        """Tests whether correct error message is returned, if input is incorrect.
        """
        response = self.test_client.get(
            "/dbgetforgivenmovierecommendedmovies?movieid=sdlkfjslfjlskjf",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")

    def test_get_recommendations_all_data_for_given_movie(self): # DELETE THIS TEST
        """Tests whether data is returned for the correct recommended movies.
        """
        response = self.test_client.get(
            "/dbgetrecommendationsalldataforgivenmovie?movieid=5445",
        )
        json_response = json.loads(response.text)
        wanted_response_1 = 'Source Code'
        wanted_response_2 = 'Limitless'

        self.assertEqual((json_response[0]["originaltitle"],
                        json_response[9]["originaltitle"]), (wanted_response_1, wanted_response_2))

    def test_get_recommendations_all_data_for_given_movie_wrong_input(self): # DELETE THIS TEST
        """Tests whether correct error message is returned, if input is incorrect.
        """
        response = self.test_client.get(
            "/dbgetrecommendationsalldataforgivenmovie?movieid=söfdslkfdjgpoipoirepwrpoewr",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")

    def test_get_for_given_movie_recommended_movies_all_data(self): # UPDATED TEST
        """Tests whether data is returned for the correct recommended movies.
        """
        response = self.test_client.get(
            "/dbgetforgivenmovierecommendedmoviesalldata?movieid=5445",
        )
        json_response = json.loads(response.text)
        wanted_response_1 = 'Source Code'
        wanted_response_2 = 'Limitless'

        self.assertEqual((json_response[0]["originaltitle"],
                        json_response[9]["originaltitle"]), (wanted_response_1, wanted_response_2))

    def test_get_for_given_movie_recommended_movies_all_data_wrong_input(self): # UPDATED TEST
        """Tests whether correct error message is returned, if input is incorrect.
        """
        response = self.test_client.get(
            "/dbgetforgivenmovierecommendedmoviesalldata?movieid=söfdslkfdjgpoipoirepwrpoewr",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")

    def test_get_recommended_books_for_given_movie(self):
        """Tests whether right number of recommended books are returned for a given movie.
        """
        response = self.test_client.get(
            "/dbgetrecommendedbooksforgivenmovie?movieid=5445",
        )
        json_response = json.loads(response.text)
        wanted_answer = 250
        self.assertEqual(len(json_response), wanted_answer)

    def test_get_recommended_books_for_given_movie_wrong_input(self):
        """Tests whether correct error message is returned, if input is incorrect.
        """
        response = self.test_client.get(
            "/dbgetrecommendedbooksforgivenmovie?movieid=9iureoit43",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")

    def test_get_recommended_books_all_data_for_given_movie(self):
        """Tests whether data is returned for the correct recommended books.
        """
        response = self.test_client.get(
            "/dbgetrecommendedbooksalldataforgivenmovie?movieid=5445",
        )
        json_response = json.loads(response.text)
        response_0_id = 2095852
        response_0_name = 'Altered Carbon (Takeshi Kovacs, #1)'
        response_9_id = 43082719
        response_9_name = 'The Drafter (The Peri Reed Chronicles, #1)'

        self.assertEqual((json_response[0]["similar_item_id"], json_response[0]["title"],
                        json_response[9]["similar_item_id"], json_response[9]["title"]),
                        (response_0_id, response_0_name, response_9_id, response_9_name))

    def test_get_recommended_books_all_data_for_given_movie_wrong_input(self):
        """Tests whether correct error message is returned, if input is incorrect.
        """
        response = self.test_client.get(
            "/dbgetrecommendedbooksalldataforgivenmovie?movieid=9iureoit43",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")
