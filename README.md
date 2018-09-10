# Coding Workshops

The backend is contained in a docker-compose instance with three images: the database, django application, and docker instance. The third image is responsible for running code in an isolated environment.

Currently, the only code transpilation that is supported is F# to JS. This is done through the Fable docker image, which is managed by [git-subrepo](https://github.com/ingydotnet/git-subrepo), a less confusing alternative to git-submodules.

## Run
`docker-compose up --build`

## Run django command
`docker-compose run web pipenv run /codingworkshops/manage.py [COMMAND]`

## Launch Docker-in-Docker shell
`docker-compose run docker sh`
THEN
`docker --host docker [COMMAND]`
