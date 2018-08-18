#!/usr/bin/env sh

# build the Django image with the backend
docker build .

# now, start the containers with docker-compose
docker-compose up -d --build

# do the first database migration
docker-compose run web python /codingworkshops/manage.py migrate --noinput

