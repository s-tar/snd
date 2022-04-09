FROM python:3.9.0-alpine3.12

WORKDIR /opt/project

RUN apk update && apk add --update --no-cache \
    build-base \
    libffi-dev \
    openldap-dev \
    postgresql-dev \
    gcc \
    python3-dev\
    jpeg-dev zlib-dev

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /opt/project/api
