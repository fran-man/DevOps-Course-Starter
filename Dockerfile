FROM python:3.8.6-slim-buster

RUN apt-get update; apt-get -y install curl; \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python; \
    mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY static /app/static
COPY templates /app/templates
COPY app.py gunicorn_config.py trello_utils.py ViewModel.py wsgi.py /app/
RUN pip3 install -r requirements.txt
EXPOSE 5000

ENTRYPOINT ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]
#ENTRYPOINT ["ls","-la","/app"]