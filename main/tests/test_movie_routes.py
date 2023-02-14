import json
import unittest
import pytest
from app import app

class TestExtentions(unittest.TestCase):
    def setUp(self):
        self.test_client = app.test_client()

    def test_get_given_movie_data(self):
        response = self.test_client.get(
            "/dbgetgivenmoviedata?movieid=210685",
        )
        json_response = json.loads(response.text)
        print(json_response)

        assert json_response["title"] == "Trailer Made"