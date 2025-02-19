SHELL := /bin/bash


build:
	docker-compose up --build

down:
	docker-compose down

run:
	docker-compose up

migrate:
	docker-compose exec backend alembic upgrade head

migrate-create:
	docker-compose exec backend alembic revision --autogenerate -m "$(name)"