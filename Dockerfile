FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /codingworkshops

RUN pip install poetry
COPY ./pyproject.toml pyproject.toml
COPY ./poetry.lock poetry.lock
RUN poetry install --no-dev

COPY ./codingworkshops codingworkshops
COPY ./manage.py .

CMD poetry run ./manage.py runserver 0.0.0.0:8000
EXPOSE 8000


