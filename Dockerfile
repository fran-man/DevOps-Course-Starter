FROM python:3.8.6-slim-buster as base

RUN apt-get update; apt-get -y install curl; \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python; \
    mkdir /app
WORKDIR /app
EXPOSE 5000

FROM base as development
COPY requirements-dev.txt /app
RUN pip3 install -r requirements-dev.txt; rm requirements-dev.txt
COPY static /app/static
COPY templates /app/templates

ENTRYPOINT ["python", "/app/app.py"]

FROM base as production
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY static /app/static
COPY templates /app/templates
COPY app.py gunicorn_config.py trello_utils.py ViewModel.py wsgi.py /app/

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]