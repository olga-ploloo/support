FROM python:3.10

# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1
ENV DOCKER 1

# setting work directory
WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt /app

# install dependencies
RUN pip install -r requirements.txt

COPY . /app

# lint
#RUN flake8 --ignore=E501,F401 .