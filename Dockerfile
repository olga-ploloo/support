FROM python:3.10

# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1
ENV DOCKER 1

# setting work directory
WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

# install dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . /app

# lint
#RUN flake8 --ignore=E501,F401 .