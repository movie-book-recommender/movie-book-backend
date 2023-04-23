#!/bin/bash
export DATABASE_URL="postgresql://user:password@localhost:5432/mvbkdb"
/usr/bin/gunicorn --workers 3 --bind unix:/var/www/mvbkbackend.sock wsgi:app
