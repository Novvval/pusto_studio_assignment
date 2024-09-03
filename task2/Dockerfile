FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off

RUN pip install -r requirements.txt
COPY ./src .
CMD python manage.py runserver 0.0.0.0:8000
