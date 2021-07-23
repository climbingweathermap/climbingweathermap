.DEFAULT_GOAL := serve
.PHONY: serve flask docker

serve:
	cd frontend && npm run compile:sass
	cd frontend && npm run serve

flask:
	cd backend && poetry run python -m flask run

docker:
	docker-compose build
	docker-compose up






