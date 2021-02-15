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
RUN curl -sSL https://dl.google.com/linux/direct/google-chromestable_current_amd64.deb -o chrome.deb; \
    apt-get install ./chrome.deb -y; \
    rm ./chrome.deb

RUN mkdir /chromedriver
WORKDIR /chromedriver

RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE`; \
    echo "Installing chromium webdriver version ${LATEST}"; \
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip; \
    apt-get install unzip -y; \
    unzip ./chromedriver_linux64.zip

RUN sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list; \
    apt-get update; \
    apt-get -y install libglib2.0 libnss3 libxcb-randr0-dev libxcb-xtest0-dev libxcb-xinerama0-dev libxcb-shape0-dev libxcb-xkb-dev

WORKDIR /app

RUN useradd -ms /bin/bash tester
USER tester

ENTRYPOINT [ "/root/.poetry/bin/poetry", "run", "pytest" ]
#ENTRYPOINT [ "/chromedriver/chromedriver", "--version" ]
#ENTRYPOINT ["whereis", "google-chrome"]