# Movie-Book-Backend

![Main workflow](https://github.com/movie-book-recommender/movie-book-backend/workflows/CI/badge.svg)

## Purpose of the repository

This repository contains the code, tests, CI/CD pipe, and documentation for the backend of the Movie Book Recommender application. Application's front end and the guidelines and documentation for the project in general are available in the [Movie Book Recommender Project repository](https://github.com/movie-book-recommender/movie-book-recommender-project). Here, only the topics specific to the backend are covered. 

## Scope of the backend

Backend for the Movie Book Recommender project contains, e.g.
* [The backend application](app.py) that runs in cPouta
* [Instructions](documentation/backend.md) with which the project's virtual machine was set up and the Postgres database was established in the production server in cPouta. 
* Tools and scripts with which the database tables have been [created](documentation/create_db.sql) and [populated](documentation/csc_json_to_csv_to_psql.sh).
* Instructions how to develop and test the backend APIs (see below). 

## Architecture

To be added

## Key dependencies

flask, flask_sqlalchemy, pytest, unittest, coverage

## Development

To develop the backend:
- Clone this repository
- Install dependencies with

```
pip install flask flask_sqlalchemy pytest unittest
```

- Set up connection to the database in cPouta
```
export "DATABASE_URL={{ database url from a team member }}"
```
- You can run the backend locally with

```
flask run
```

Follow this [guide for branch workflow](https://github.com/movie-book-recommender/movie-book-recommender-project/blob/main/Documentation/workflow/branch_workflow.md) when developing.

## Testing locally

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

## To do's

- Project main branch
- Github actions to update the newest version only when merging
- More tests for different API's
- Add coverage reporting to the yml file

## Licensing

The application is licensed under the MIT License.