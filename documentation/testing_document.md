# Testing Document

This program is developed and tested using Python 3.10 or newer. Testing is done with pytest and all tests can be run with

``` python3 -m pytest ```

## Unit Testing

Testing is based on unit tests that use mockup client so that the testing environment is as close to end to end as possible.

``` self.test_client = app.test_client() ```

Creates a mockup flask app that pytest can use to test routes.

For example: 

``` response = self.test_client.get("/dbgettop10newestbooks") ```

Then we parse the json from the response

``` json_response = json.loads(response.text) ```

And see if the response is what it is supposed to be

``` wanted_response = "180 Seconds" ```
        
``` self.assertEqual(json_response[0]["title"], wanted_response) ```

Every route is tested with correct and incorrect inputs to make sure the program does not crash.

All tests are in [main/tests](https://github.com/movie-book-recommender/movie-book-backend/tree/main/main/tests)

## Test Coverage

The current test coverage can be reviewed [here](https://app.codecov.io/gh/movie-book-recommender/movie-book-backend)

To make sure of the quality of the code, it is suggested that the code coverage is kept better than 70 percent.


