.DEFAULT_GOAL := local
.PHONY: local, tox

local: tox
	docker-compose build -f docker-compose.dev.yml
	docker-compose up

tox:
	cd backend && poetry run python -m tox -e py39




