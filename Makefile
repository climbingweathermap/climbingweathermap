.DEFAULT_GOAL := serve
.PHONY: serve flask docker

serve:
	cd frontend && npm run compile:sass
	cd frontend && npm run serve

flask:
	cd backend && poetry run python -m flask run  --eager-loading

docker:
	-docker rmi weathermap -f
	docker build --tag weathermap .
	docker images




