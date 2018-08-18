FROM python:3.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /codingworkshops

RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /codingworkshops/Pipfile
RUN pipenv install --deploy --system --skip-lock --dev

COPY . /codingworkshops/
