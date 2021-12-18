.DEFAULT_GOAL := local
.PHONY: local, tox

local: tox
	docker-compose -f docker-compose.dev.yml build 
	docker-compose -f docker-compose.dev.yml up 

tox:
	cd backend && poetry run python -m tox -e py39




