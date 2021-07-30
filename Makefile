.DEFAULT_GOAL := local
.PHONY: local deploy

local:
	docker-compose build
	docker-compose up

deploy:
	eb deploy





