build:
	docker-compose build

migrate: build
	docker-compose run --rm app python /app/manage.py migrate

up: migrate
	docker-compose up -d

app-down:
	docker-compose stop app && docker-compose rm app

app-logs:
	docker-compose logs -f app

deploy: build migrate app-down up

shell:
	docker-compose -f ./docker-compose.yaml -f ./docker-compose-dev.yaml run app bash

makemigrations: build
	docker-compose -f ./docker-compose.yaml -f ./docker-compose-dev.yaml run --rm app python /app/manage.py makemigrations

down:
	docker-compose -f ./docker-compose.yaml -f ./docker-compose-dev.yaml down

clean:
	docker-compose -f ./docker-compose.yaml -f ./docker-compose-dev.yaml down -v
