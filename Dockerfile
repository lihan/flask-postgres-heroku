FROM python:3.6.6-alpine3.8

LABEL maintainer="llihan673@gmail.com"

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev

COPY requirements.txt /requirements.txt

# Installing required modules
RUN pip3 --no-cache-dir install -r /requirements.txt

ENV APP_ROOT '/application'
RUN mkdir -p $APP_ROOT

WORKDIR $APP_ROOT
COPY . $APP_ROOT

EXPOSE 5000

ENTRYPOINT gunicorn \
        --access-logfile="-"                   \
        --error-logfile="-"                    \
        --bind=0.0.0.0:5000                    \
        --worker-class=sync                    \
        --workers=1                            \
        --keep-alive=10                        \
        --graceful-timeout=10                  \
        app:app
