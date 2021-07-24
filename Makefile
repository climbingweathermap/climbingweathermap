.DEFAULT_GOAL := test
.PHONY: test deploy

test:
	docker-compose build
	docker-compose up

deploy:
	eb deploy





