FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y nginx-full locales \
    && sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen \
    && true
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_ALL ru_RU.UTF-8
ENV TZ 'Europe/Moscow'

RUN rm -rf /etc/nginx/sites-enabled/*

COPY conf/*.nginx /etc/nginx/modules-enabled/
COPY conf/conf.d/*.nginx /etc/nginx/conf.d/
COPY conf/sites-enabled/*.nginx /etc/nginx/sites-enabled/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
