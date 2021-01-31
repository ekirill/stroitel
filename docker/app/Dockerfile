FROM python:3.7-slim

ADD docker/app/entrypoint.sh /entrypoint.sh

EXPOSE 8000
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=stroitel.settings
ENTRYPOINT ["/entrypoint.sh"]

RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    iproute2 \
    libpcre3-dev \
    libpq-dev \
    netcat \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && true

ADD requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
RUN chmod +x /entrypoint.sh \
    && mkdir /app/ \
    && true

ENV UWSGI_WSGI_FILE=/app/stroitel/wsgi.py
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4
ENV UWSGI_STATIC_MAP="/static/=/app/htdocs/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

WORKDIR /app/
ADD . /app/
RUN DATABASE_URL='' python manage.py collectstatic --noinput

CMD ["uwsgi", "--show-config"]
