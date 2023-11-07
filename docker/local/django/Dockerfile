from python:3.10.0-slim-buster


ENV APP_HOME=/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME



LABEL maintainer='a@a.com'
LABEL description='a@a.com'

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHOONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev \
    && apt-get install -y gettext \
    && apt-get install -y netcat gcc postgresql \
    && apt-get purge --auto-remove -y -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


RUN pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./docker/local/django/entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN chmod +x /start


COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/local/django/flower/start /start-flower
RUN chmod +x /start-flower

ENTRYPOINT ["/entrypoint"]

