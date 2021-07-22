.DEFAULT_GOAL := serve
.PHONY: serve flask build

serve:
	cd frontend && npm run compile:sass
	cd frontend && npm run serve

flask:
	cd backend && poetry run flask run

build:
	cd frontend && npm run build




