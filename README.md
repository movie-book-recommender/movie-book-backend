# Movie-Book-Backend

![Main workflow](https://github.com/movie-book-recommender/movie-book-backend/workflows/CI/badge.svg)

[![codecov](https://codecov.io/gh/movie-book-recommender/movie-book-backend/branch/main/graph/badge.svg?token=OJ4LB2MBIL)](https://codecov.io/gh/movie-book-recommender/movie-book-backend)

## Purpose of the Repository

This repository contains the code, tests, CI/CD pipe, and documentation for the backend of the Movie Book Recommender application. Application's front end and the guidelines and documentation for the project in general are available in the [Movie Book Recommender Project repository](https://github.com/movie-book-recommender/movie-book-recommender-project). Here, only the topics specific to the backend are covered. 

## Contents of the Repository

Backend for the Movie Book Recommender project contains
* Code for [the backend application](app.py) that runs in cPouta
* [Instructions](/documentation/backend_developer_start.md) how to start developing and testing the backend APIs.
* [Technical instructions](documentation/backend.md) that show how the project's virtual machine was set up, and how the Postgres database was established in the production server in cPouta.
* [Documentation of the architecture](documentation/architecture.md)
* Instructions contain links to tools and scripts showing how, e.g., the database tables have been [created](documentation/create_db.sql) and [populated](documentation/csc_json_to_csv_to_psql.sh).
* [Documentation of back-end tests](documentation/testing_document.md)

## Licensing

The application is licensed under the MIT License. 
