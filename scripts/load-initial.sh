#! /bin/bash

docker-compose run web poetry run /codingworkshops/manage.py loaddata default
docker-compose run web poetry run /codingworkshops/manage.py loaddata nico


