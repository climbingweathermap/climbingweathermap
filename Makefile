.DEFAULT_GOAL := serve
.PHONY: serve flask build

serve:
	npm run compile:sass
	npm run serve

flask:
	poetry run Flask run

build:
	npm run build


