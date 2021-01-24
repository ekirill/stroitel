migrate:
	docker-compose run --rm app python /app/manage.py migrate

build:
	docker-compose build

push:
	docker push ekirill.ru:5000/stroitel_app
