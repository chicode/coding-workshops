FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /codingworkshops

RUN pip install pipenv
COPY ./Pipfile Pipfile
COPY ./Pipfile.lock Pipfile.lock
RUN pipenv install

COPY ./codingworkshops codingworkshops
COPY ./manage.py .

CMD pipenv run ./manage.py runserver 0.0.0.0:8000
EXPOSE 8000


