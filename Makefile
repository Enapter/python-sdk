.PHONY: default
default:

.PHONY: install-deps
install-deps:
	pipenv install --dev

.PHONY: update-deps
update-deps:
	pipenv update --dev

.PHONY: check
check: lint test

.PHONY: lint
lint:
	pipenv run black --check .
	pipenv run isort --check .
	pipenv run pyflakes .

.PHONY: test
test: run-unit-tests

.PHONY: run-unit-tests
run-unit-tests:
	pipenv run pytest -vv --cov --cov-report term-missing tests/unit

.PHONY: get-pipenv
get-pipenv:
	curl https://raw.githubusercontent.com/pypa/pipenv/master/get-pipenv.py | python

.PHONY: upload-to-pypi
upload-to-pypi: dist
ifndef PYPI_API_TOKEN
	$(error PYPI_API_TOKEN is not defined)
endif
	@pipenv run twine upload \
		--username __token__ \
		--password $(PYPI_API_TOKEN) \
		$</*

dist.tar: dist
	rm --force $@
	tar --create --file $@ $<

.PHONY: dist
dist:
	pipenv run python setup.py bdist_wheel
