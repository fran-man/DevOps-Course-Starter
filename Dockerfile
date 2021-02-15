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
COPY . ./

ENTRYPOINT [ "/root/.poetry/bin/poetry", "run", "gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]

FROM base as test

ENTRYPOINT ["/root/.poetry/bin/poetry", "run", "pytest"]