NAME := utils

DATA := $(CURDIR)/data
DIST := $(CURDIR)/dist
DOCS := $(CURDIR)/docs

DOCS_SRC_LIST += $(DOCS)/awesome-github.md
DOCS_SRC_LIST += $(DOCS)/awesome-websites.md
DOCS_SRC_LIST += $(DOCS)/index.md

OS   != echo $(RUNNER_OS) | tr '[:upper:]' '[:lower:]'
ARCH != echo $(RUNNER_ARCH) | tr '[:upper:]' '[:lower:]'

ifneq ($(and $(OS), $(ARCH)), )
	NAME := $(NAME)-$(OS)-$(ARCH)
endif

ifeq ($(OS), windows)
	EXE := .exe
else
	EXE :=
endif

EXECUTABLE := $(DIST)/$(NAME)$(EXE)

all:

dist: $(EXECUTABLE)

docs: $(DOCS_SRC_LIST)

docs-build: $(DOCS_SRC_LIST)
	mkdocs build

docs-serve: $(DOCS_SRC_LIST)
	mkdocs serve

docs-gh-deploy: $(DOCS_SRC_LIST)
	mkdocs gh-deploy

poetry: $(CURDIR)/poetry.lock $(CURDIR)/requirements.txt

pretty: prettier pretty-python

prettier: | $(CURDIR)/.gitignore
	prettier --write --ignore-path $| $(CURDIR)

pretty-python:
	isort --profile black $(CURDIR)
	black $(CURDIR)

$(CURDIR)/poetry.lock: pyproject.toml
	poetry lock

$(CURDIR)/requirements.txt: $(CURDIR)/poetry.lock
	poetry export --output requirements.txt --without-hashes --without-urls

$(DOCS)/awesome-github.md: $(DATA)/github.yaml
	poetry run utils sort github --in-place --markdown $@ $<
	prettier --write $<
	prettier --write $@

$(DOCS)/awesome-websites.md: $(DATA)/websites.yaml
	poetry run utils sort website --in-place --markdown $@ $<
	prettier --write $<
	prettier --write $@

$(DOCS)/index.md:
	typer utils.cmd utils docs --output $@
	prettier --write $@

$(EXECUTABLE): $(CURDIR)/main.py
	pyinstaller --onefile --name $(NAME) $<
