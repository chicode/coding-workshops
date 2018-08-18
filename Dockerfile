FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /codingworkshops

RUN pip install pipenv
COPY ./Pipfile
COPY ./Pipfile.lock
RUN pipenv install

COPY . /codingworkshops/
