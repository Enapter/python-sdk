.PHONY: default
default:

.PHONY: install-deps
install-deps:
	uv sync

.PHONY: update-deps
update-deps:
	uv sync --upgrade

.PHONY: check
check: lint test

.PHONY: lint
lint: lint-black lint-isort lint-pyflakes lint-mypy

.PHONY: lint-black
lint-black:
	uv run black --check --diff .

.PHONY: lint-isort
lint-isort:
	uv run isort --check .

.PHONY: lint-pyflakes
lint-pyflakes:
	uv run pyflakes src tests examples

.PHONY: lint-mypy
lint-mypy:
	uv run mypy tests
	uv run mypy src/enapter

.PHONY: test
test: test-unit test-integration

.PHONY: test-unit
test-unit:
	uv run pytest -vv --cov=enapter --cov-report term-missing tests/unit

.PHONY: test-integration
test-integration:
	uv run pytest -vv --capture=no tests/integration

.PHONY: upload-to-pypi
upload-to-pypi: dist
ifndef PYPI_API_TOKEN
	$(error PYPI_API_TOKEN is not defined)
endif
	@uv publish \
		--token $(PYPI_API_TOKEN) \
		$</*

dist.tar: dist
	rm --force $@
	tar --create --file $@ $<

.PHONY: dist
dist:
	rm -rf dist
	uv build

RE_SEMVER = [0-9]+.[0-9]+.[0-9]+(-[a-z0-9]+)?

.PHONY: bump-version
bump-version:
ifndef V
	$(error V is not defined)
endif
	sed -E -i 's/__version__ = "$(RE_SEMVER)"/__version__ = "$(V)"/g' src/enapter/__init__.py
	uv lock
	grep -E --files-with-matches --recursive "enapter==$(RE_SEMVER)" README.md examples \
		| xargs -n 1 sed -E -i "s/enapter==$(RE_SEMVER)/enapter==$(V)/g"
	git add .
	git commit -m "bump version to $(V)"
	git tag "v$(V)"


DOCKER_IMAGE_TAG ?= enapter/python-sdk:dev

.PHONY: docker-image
docker-image:
	docker build -t $(DOCKER_IMAGE_TAG) .
