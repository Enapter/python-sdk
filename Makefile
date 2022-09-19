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
	pipenv run pytest tests

.PHONY: get-pipenv
get-pipenv:
	curl https://raw.githubusercontent.com/pypa/pipenv/master/get-pipenv.py | python

.PHONY: upload-to-test-pypi
upload-to-test-pypi:
ifndef TEST_PYPI_API_TOKEN
	$(error TEST_PYPI_API_TOKEN is not defined)
endif
	@$(MAKE) \
		PYPI_API_TOKEN=$(TEST_PYPI_API_TOKEN) \
		PYPI_REPOSITORY_URL=https://test.pypi.org/legacy/ \
		upload-to-pypi

.PHONY: upload-to-pypi
upload-to-pypi: dist
ifndef PYPI_API_TOKEN
	$(error PYPI_API_TOKEN is not defined)
endif
	@pipenv run twine upload \
		$(if $(PYPI_REPOSITORY_URL),--repository-url $(PYPI_REPOSITORY_URL),) \
		--username __token__ \
		--password $(PYPI_API_TOKEN) \
		$</*

dist.tar: dist
	rm --force $@
	tar --create --file $@ $<

.PHONY: dist
dist:
	pipenv run python setup.py bdist_wheel
