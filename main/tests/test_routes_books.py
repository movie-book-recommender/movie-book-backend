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

        self.assertEqual(json_response["value"], "not available")
