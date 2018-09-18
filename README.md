# Coding Workshops

## Explainer

The backend is contained in a docker-compose instance with three images: the database, django application, and docker instance. The third image is responsible for running code in an isolated environment.

Currently, the only code transpilation that is supported is F# to JS. This is done through the Fable docker image, which is managed by [git-subrepo](https://github.com/ingydotnet/git-subrepo), a less confusing alternative to git-submodules.


## Basic setup
0. Install docker and docker-compose

1. Create a root `.env` file by copying `.env.example`

2. Build the image
`docker build .`

3. Run Docker Compose process
`docker-compose up`

4. In a different window, load some data
`bash scripts/load-initial.sh`


## Misc

## Run Docker Compose in detached mode, which means that it runs in the background
`docker-compose up -d`

## Run django command
`bash scripts/run-django-script [COMMAND]`

## Launch Docker-in-Docker shell
`docker-compose run docker sh`
THEN
`docker --host docker [COMMAND]`
