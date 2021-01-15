FROM python:3.8.6-slim-buster as base

RUN apt-get update; apt-get -y install curl; \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python; \
    mkdir /app
WORKDIR /app
EXPOSE 5000

FROM base as development
COPY pyproject.toml /app
RUN export PATH=$PATH:$HOME/.poetry/bin; poetry install --no-dev

ENTRYPOINT [ "/root/.poetry/bin/poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base as production
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY static /app/static
COPY templates /app/templates
COPY app.py gunicorn_config.py trello_utils.py ViewModel.py wsgi.py /app/

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]