#!/usr/bin/env bash

set -ex

echo "Waiting postgres to launch"

while ! nc -z db 5432; do
  sleep 1
done

echo "postgres launched"

exec "$@"
