build:
	docker-compose build

migrate: build
	docker-compose run --rm app python /app/manage.py migrate

up: migrate
	docker-compose up -d
