build:
	docker-compose -p stroitel build

migrate: build
	docker-compose -p stroitel run --rm app python /app/manage.py migrate

up: migrate
	docker-compose -p stroitel up -d

app-down:
	docker-compose -p stroitel stop app && docker-compose rm app

app-logs:
	docker-compose -p stroitel logs -f app

deploy: build migrate app-down up

shell:
	docker-compose -p stroitel -f ./docker-compose.yaml -f ./docker-compose-dev.yaml run app bash

nginx-enter:
	docker-compose -p stroitel -f ./docker-compose.yaml -f ./docker-compose-dev.yaml exec nginx bash

makemigrations: build
	docker-compose -p stroitel -f ./docker-compose.yaml -f ./docker-compose-dev.yaml run --rm app python /app/manage.py makemigrations

down:
	docker-compose -p stroitel -f ./docker-compose.yaml -f ./docker-compose-dev.yaml down

clean:
	docker-compose -p stroitel -f ./docker-compose.yaml -f ./docker-compose-dev.yaml down -v

dev-run:
	docker-compose -p stroitel -f ./docker-compose.yaml -f ./docker-compose-dev.yaml up

db-dump:
	docker-compose -p stroitel -f ./docker-compose.yaml exec db pg_dump -U stroi -d stroitel --format=plain > ./dump.sql

db-restore:
	docker cp ~/stroitel_dump.sql stroitel_db_1:/dump.sql
	docker-compose -p stroitel -f ./docker-compose.yaml stop app;
	docker-compose -p stroitel -f ./docker-compose.yaml exec db psql -U stroi -d postgres -c 'DROP DATABASE stroitel';
	docker-compose -p stroitel -f ./docker-compose.yaml exec db psql -U stroi -d postgres -c 'CREATE DATABASE stroitel';
	docker-compose -p stroitel -f ./docker-compose.yaml exec db psql -U stroi -d stroitel -f /dump.sql
	docker-compose -p stroitel -f ./docker-compose.yaml up -d;

db-scp:
	scp ekirill@ekirill.ru:/mnt/storage/stroitel/dump.sql.gz ~/stroitel_dump.sql.gz
	gunzip ~/stroitel_dump.sql.gz
	docker-compose -p stroitel -f ./docker-compose.yaml up -d db
	sleep 20

db-clone: db-scp db-restore
