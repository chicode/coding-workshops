#! /bin/bash

docker-compose run web pipenv run /codingworkshops/manage.py "$@"
