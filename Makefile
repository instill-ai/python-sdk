PROJECT := instill-sdk
PACKAGE := instill
MODULES := $(wildcard $(PACKAGE)/*.py)

# MAIN TASKS ##################################################################

.PHONY: all
all: doctor format check test mkdocs ## Run all tasks that determine CI status

.PHONY: dev
dev: install .clean-test ## Continuously run CI tasks when files change
	poetry run sniffer

# SYSTEM DEPENDENCIES #########################################################

.PHONY: doctor
doctor: ## Confirm system dependencies are available
	bin/verchew

# PROJECT DEPENDENCIES ########################################################

VIRTUAL_ENV ?= .venv
DEPENDENCIES := $(VIRTUAL_ENV)/.poetry-$(shell bin/checksum pyproject.toml poetry.lock)

.PHONY: install
install: $(DEPENDENCIES) .cache ## Install project dependencies

$(DEPENDENCIES): poetry.lock
	@ rm -rf $(VIRTUAL_ENV)/.poetry-*
	@ rm -rf ~/Library/Preferences/pypoetry
	@ poetry config virtualenvs.in-project true
	poetry install
	@ touch $@

ifndef CI
poetry.lock: pyproject.toml
	poetry lock
	@ touch $@
endif

.cache:
	@ mkdir -p .cache

.PHONY: get-proto
get-proto:
	@ git submodule update --init --recursive

.PHONY: update-proto
update-proto:
	@ git submodule update --remote --merge

.PHONY: update-specs
update-specs:
	@ bash bin/specs

# TEST ########################################################################

RANDOM_SEED ?= $(shell date +%s)
FAILURES := .cache/pytest/v/cache/lastfailed

PYTEST_OPTIONS := --random --random-seed=$(RANDOM_SEED)
ifndef DISABLE_COVERAGE
PYTEST_OPTIONS += --cov=$(PACKAGE)
endif
ifdef CI
PYTEST_OPTIONS += --cov-report=xml
endif
PYTEST_RERUN_OPTIONS := --last-failed --exitfirst

.PHONY: test-unit
test-unit: install
	@ ( mv $(FAILURES) $(FAILURES).bak || true ) > /dev/null 2>&1
	poetry run pytest $(PACKAGE) $(PYTEST_OPTIONS)
	@ ( mv $(FAILURES).bak $(FAILURES) || true ) > /dev/null 2>&1
ifndef DISABLE_COVERAGE
	poetry run coveragespace update unit
endif

.PHONY: test
test: test-unit

.PHONY: read-coverage
read-coverage:
	open htmlcov/index.html

# CHECK #######################################################################

.PHONY: format
format: install
	poetry run isort $(PACKAGE) notebooks
	poetry run black $(PACKAGE) notebooks
	@ echo

.PHONY: check
check: install format ## Run formatters, linters, and static analysis
ifdef CI
	git diff --exit-code
endif
	poetry run mypy $(PACKAGE)
	poetry run pylint $(PACKAGE) --rcfile=.pylint.ini
	poetry run pydocstyle $(PACKAGE)

# DOCUMENTATION ###############################################################

MKDOCS_INDEX := site/index.html

.PHONY: docs
docs: mkdocs ## Generate documentation
ifndef CI
	@ eval "sleep 3; open http://127.0.0.1:8000" &
	poetry run mkdocs serve
endif

.PHONY: mkdocs
mkdocs: install $(MKDOCS_INDEX)
$(MKDOCS_INDEX): docs/requirements.txt mkdocs.yml docs/*.md
	@ mkdir -p docs/about
	@ cd docs && ln -sf ../README.md index.md
	@ cd docs/about && ln -sf ../../CHANGELOG.md changelog.md
	@ cd docs/about && ln -sf ../../.github/CONTRIBUTING.md contributing.md
	@ cd docs/about && ln -sf ../../LICENSE.md license.md
	poetry run mkdocs build --clean --strict

docs/requirements.txt: poetry.lock
	@ poetry export --with dev --without-hashes | grep mkdocs > $@
	@ poetry export --with dev --without-hashes | grep pygments >> $@
	@ poetry export --with dev --without-hashes | grep jinja2 >> $@

# DEMO ########################################################################

.PHONY: run
run: install ## Start the program
	poetry run python $(PACKAGE)/__main__.py

.PHONY: shell
shell: install ## Launch an IPython session
	poetry run ipython --ipython-dir=notebooks

# BUILD #######################################################################

DIST_FILES := dist/*.tar.gz dist/*.whl
EXE_FILES := dist/$(PACKAGE).*

.PHONY: dist
dist: install get-proto $(DIST_FILES)
$(DIST_FILES): $(MODULES) pyproject.toml
	rm -f $(DIST_FILES)
	poetry build

.PHONY: exe
exe: install $(EXE_FILES)
$(EXE_FILES): $(MODULES) $(PACKAGE).spec
	poetry run pyinstaller $(PACKAGE).spec --noconfirm --clean

$(PACKAGE).spec:
	poetry run pyi-makespec $(PACKAGE)/__main__.py --onefile --windowed --name=$(PACKAGE)

# RELEASE #####################################################################

.PHONY: upload
upload: dist ## Upload the current version to PyPI
	git diff --name-only --exit-code
ifeq (${TEST_REPO}, true)
	poetry publish -r testpypi
else
	poetry publish
endif

# CLEANUP #####################################################################

.PHONY: clean
clean: .clean-build .clean-docs .clean-test .clean-install ## Delete all generated and temporary files

.PHONY: clean-all
clean-all: clean
	rm -rf $(VIRTUAL_ENV)

.PHONY: .clean-install
.clean-install:
	find $(PACKAGE) -name '__pycache__' -delete
	rm -rf *.egg-info

.PHONY: .clean-test
.clean-test:
	rm -rf .cache .pytest .coverage htmlcov

.PHONY: .clean-docs
.clean-docs:
	rm -rf docs/*.png site

.PHONY: .clean-build
.clean-build:
	rm -rf *.spec dist build

# HELP ########################################################################

.PHONY: help
help: install
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
