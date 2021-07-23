# syntax=docker/dockerfile:1

FROM python:3.9.6-slim-buster

ENV FLASK_APP=app

RUN mkdir /app 
COPY /backend /app

COPY backend/pyproject.toml /app 

WORKDIR /app
RUN pip install "poetry==1.1.7"

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 5000

CMD poetry run flask run

