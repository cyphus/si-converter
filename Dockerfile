FROM ubuntu:bionic

MAINTAINER Phillip Bailey <phillip@bailey.st>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y \
    python3-pip python3-dev uwsgi-plugin-python3 \
    nginx supervisor

COPY nginx/flask.conf /etc/nginx/sites-available/
COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY . /var/www/app

RUN mkdir -p /var/log/nginx/app /var/log/uwsgi/app /var/log/supervisor \
    && rm /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf \
    && echo "daemon off;" >> /etc/nginx/nginx.conf \
    && pip3 install -r /var/www/app/units/requirements.txt \
    && pip3 install -e /var/www/app \
    && chown -R www-data:www-data /var/www/app \
    && chown -R www-data:www-data /var/log


CMD ["/usr/bin/supervisord"]
