# Development Instructions for the Backend

This describes the key actions to take to develop and tests APIs in the backend.

## Key Dependencies

The key Python packages required are:

flask, flask_sqlalchemy, pytest, unittest, coverage, psycopg2, pandas

## Development

To develop the backend:
* Clone this repository
* Install dependencies with

```
pip install flask flask_sqlalchemy pytest unittest coverage psycopg2 pandas
```

* Set up connection to the database running in cPouta
```
export DATABASE_URL="postgresql://user:password@128.214.253.51:5432/mvbkdb"
```

* You can run the backend locally with

```
flask run
```

Follow this [guide for branch workflow](https://github.com/movie-book-recommender/movie-book-recommender-project/blob/main/Documentation/workflow/branch_workflow.md) when developing.

## Database

When developing the APIs, it may be useful to see the existing data in the Postgres database. A useful software for this purpose is [pgAdmin4](https://www.pgadmin.org/download/).

## Local Testing

To run tests locally, please use the following command: 
```
python3 -m pytest
```

To get coverage report for unit tests, in console or in html, locally
```
coverage run --branch -m pytest main 
coverage report -m
coverage html
```

The test files can be seen in folder [main/tests](main/tests/).

## Local Quality Checks

To check code quality locally, please use the following command: 
```
pylint main
```
