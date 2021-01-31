build:
	docker-compose build

migrate: build
	docker-compose run --rm app python /app/manage.py migrate

up: migrate
	docker-compose up -d

shell:
	docker-compose -f ./docker-compose.yaml -f ./docker-compose-dev.yaml exec app bash

makemigrations: build
	docker-compose -f ./docker-compose.yaml -f ./docker-compose-dev.yaml run --rm app python /app/manage.py makemigrations

down:
	docker-compose -f ./docker-compose.yaml -f ./docker-compose-dev.yaml down

clean:
	docker-compose -f ./docker-compose.yaml -f ./docker-compose-dev.yaml down -v
