.PHONY: lint format


lint: format
	poetry run ruff check src/

format:
	poetry run isort src
	poetry run black src

security-baseline:
	poetry run bandit -r src

mypy:
	poetry run mypy --pretty src