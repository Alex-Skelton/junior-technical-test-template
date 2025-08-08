.PHONY: run test

run:
	poetry run flask --app main:app run --debug

test:
	poetry run python -m pytest -vvv
