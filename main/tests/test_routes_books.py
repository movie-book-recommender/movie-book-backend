"""
This module implements unit and integration tests for routes related to books.
"""
import json
import unittest
from app import app

class TestBooksRoutes(unittest.TestCase):
    """
    This class implements tests for routes related to books.
    Args:
        unittest (object): TBD
    """
    def setUp(self):
        """This is a test client that can handle get and post requests
        to test the APIs.
        """
        self.test_client = app.test_client()

    def test_get_top_10_newest_books_correct_answer(self):
        """Tests whether the query latest published book in the database.
        """
        response = self.test_client.get(
            "/dbgettop10newestbooks",
        )
        json_response = json.loads(response.text)
        wanted_response = "180 Seconds"
        self.assertEqual(json_response[0]["title"], wanted_response)

    def test_get_top_10_newest_books_incorrect_answer(self):
        """Tests whether the query latest published book in the database.
        """
        response = self.test_client.get(
            "/dbgettop10newestbooks",
        )
        json_response = json.loads(response.text)
        wanted_response = "asadad"
        self.assertNotEqual(json_response[0]["title"], wanted_response)

    def test_get_given_book_data_not_given(self):
        """Tests whether an incorrect input is detected.
        """
        response = self.test_client.get(
            "/dbgetgivenbookdata?bookid=",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")

    def test_get_given_book_data_incorrect_input(self):
        """Tests whether an incorrect input is detected.
        """
        response = self.test_client.get(
            "/dbgetgivenbookdata?bookid=sakjhdkaj",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")

    def test_get_given_book_data_incorrect_number(self):
        """Tests whether an incorrect input is detected.
        """
        response = self.test_client.get(
            "/dbgetgivenbookdata?bookid=984309438094377",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")

    def test_get_given_book_data_correct_number(self):
        """Tests whether correct book is return for a correct id.
        """
        response = self.test_client.get(
            "/dbgetgivenbookdata?bookid=44752519",
        )
        json_response = json.loads(response.text)
        wanted_response = "A Conjuring of Light (Shades of Magic, #3)"
        self.assertEqual(json_response["title"], wanted_response)

    def test_search_books_by_name_top_20(self):
        """Tests whether correct books are returned for a name search
        """
        response = self.test_client.get(
            "/dbsearchbooksbyname?input=Sookie stackhouse",
        )
        json_response = json.loads(response.text)
        wanted_response = "A Touch of Dead (Sookie Stackhouse, #4.1, #4.3, #5.1, #7.1, #8.1)"

        self.assertEqual(json_response[0]["title"], wanted_response)

    def test_search_books_by_name_top_20_incorrect_input(self):
        """Tests whether an incorrect input is detected.
        """
        response = self.test_client.get(
            "/dbsearchbooksbyname?input=oeritpoiew",
        )
        json_response = json.loads(response.text)
        wanted_answer = []
        self.assertEqual(json_response, wanted_answer)
    
    def test_get_top_10_highest_rated_books(self):
        """Testing the top 10 books function
        """
        response = self.test_client.get(
            "/dbgettop10highestratedbooks",
        )
        json_response = json.loads(response.text)
        self.assertEqual(len(json_response), 10)

    def test_get_for_given_book_recommended_books(self):
        """Tests whether 10 recommended books are returned for a given book.
        """
        response = self.test_client.get(
            "/dbgetforgivenbookrecommendedbooks?bookid=150259",
        )
        json_response = json.loads(response.text)

        self.assertEqual(len(json_response), 10)

    def test_get_for_given_book_recommended_books_wrong_input(self):
        """Tests whether correct error message is returned, if input is incorrect.
        """
        response = self.test_client.get(
            "/dbgetforgivenbookrecommendedbooks?bookid=sdlkfjslfjlskjf",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")

    def test_get_for_given_book_recommended_books_all_data(self):
        """Tests whether data is returned for the correct recommended books.
        """
        response = self.test_client.get(
            "/dbgetforgivenbookrecommendedbooksalldata?bookid=150259",
        )
        json_response = json.loads(response.text)
        wanted_response_1 = 'Doctor Sleep'
        wanted_response_2 = 'Joyland'

        self.assertEqual((json_response[0]["title"], json_response[9]["title"]), (wanted_response_1, wanted_response_2))

    def test_get_for_given_book_recommended_books_all_data_wrong_input(self):
        """Tests whether correct error message is returned, if input is incorrect.
        """
        response = self.test_client.get(
            "/dbgetforgivenbookrecommendedbooksalldata?bookid=söfdslkfdjgpoipoirepwrpoewr",
        )
        json_response = json.loads(response.text)

        self.assertEqual(json_response["value"], "not available")
