# syntax=docker/dockerfile:1

FROM python:3.9.6-slim-buster

RUN mkdir /app 
COPY ./ /app

COPY ./pyproject.toml /app 

WORKDIR /app
RUN pip install "poetry==1.1.7"

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


CMD ["gunicorn", "-w", "3", "-b", ":5000", "-t", "360", "--reload", "wsgi:app"]

