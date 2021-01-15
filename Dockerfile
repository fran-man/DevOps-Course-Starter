FROM python:3.8.6-slim-buster as base

RUN apt-get update; apt-get -y install curl; \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python; \
    mkdir /app
WORKDIR /app
EXPOSE 5000
COPY pyproject.toml /app
RUN export PATH=$PATH:$HOME/.poetry/bin; poetry install --no-dev

FROM base as development

ENTRYPOINT [ "/root/.poetry/bin/poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base as production
COPY static /app/static
COPY templates /app/templates
COPY app.py gunicorn_config.py trello_utils.py ViewModel.py wsgi.py /app/

ENTRYPOINT [ "/root/.poetry/bin/poetry", "run", "gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]