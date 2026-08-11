.PHONY: install test run load-test validate all

install:
	pip install -r requirements.txt

test:
	python -m pytest -q

run:
	uvicorn app.main:app --reload --env-file .env

load-test:
	python scripts/load_test.py --concurrency 2

validate:
	python scripts/validate_logs.py
	python scripts/validate_dashboard.py

all: test validate
