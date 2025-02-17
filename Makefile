SHELL := /bin/bash


build:
	docker compose up --build

down:
	docker-compose down

run:
	docker compose up

bash:
	docker exec -it $$(docker ps -qf "ancestor=$(IMAGE_NAME)") /bin/sh

