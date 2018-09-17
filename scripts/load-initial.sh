#! /bin/bash

docker-compose run web pipenv run /codingworkshops/manage.py loaddata default
docker-compose run web pipenv run /codingworkshops/manage.py loaddata nico

