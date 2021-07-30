.DEFAULT_GOAL := local
.PHONY: local deploy, tox

local:
	docker-compose build
	docker-compose up

deploy:
	eb deploy


tox:
	cd backend && poetry run python -m tox -e py39




