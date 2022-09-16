.PHONY: default
default:

.PHONY: install-deps
install-deps:
	pipenv install --dev

.PHONY: update-deps
update-deps:
	pipenv update

.PHONY: check
check: lint test

.PHONY: lint
lint:
	pipenv run black --check .
	pipenv run isort --check .
	pipenv run pyflakes .

.PHONY: test
test:
	pipenv run pytest
