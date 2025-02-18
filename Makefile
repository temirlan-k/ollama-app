SHELL := /bin/bash


build:
	docker-compose up --build

down:
	docker-compose down

run:
	docker-compose up

