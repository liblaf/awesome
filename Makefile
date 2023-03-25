NAME := utils.py

BIN   := $(HOME)/.local/bin
BUILD := $(CURDIR)/build
DATA  := $(CURDIR)/data
DIST  := $(CURDIR)/dist
DOCS  := $(CURDIR)/docs
SITE  := $(CURDIR)/site

OS   := $(shell echo $(RUNNER_OS)   | tr '[:upper:]' '[:lower:]')
ARCH := $(shell echo $(RUNNER_ARCH) | tr '[:upper:]' '[:lower:]')
ifeq ($(OS), windows)
	EXE := .exe
else
	EXE :=
endif
TARGET := $(DIST)/$(NAME)$(EXE)

GITHUB_TOKEN :=

build: $(TARGET)

clean:
	$(RM) --recursive $(BUILD)
	$(RM) --recursive $(DIST)
	$(RM) --recursive $(SITE)
	$(RM) $(CURDIR)/*.spec

docs: $(DOCS)/awesome-github.md $(DOCS)/index.md

docs-build: $(CURDIR)/mkdocs.yaml docs
	mkdocs build --config-file $< --site-dir $(SITE)

docs-gh-deploy: $(CURDIR)/mkdocs.yaml docs
	mkdocs gh-deploy --force --no-history --config-file $< --site-dir $(SITE)

docs-serve: $(CURDIR)/mkdocs.yaml docs
	mkdocs serve --config-file $<

install: $(TARGET) | $(BIN)
	install --target-directory=$(BIN) $<

pretty:
	isort --profile black $(CURDIR)
	black $(CURDIR)
	prettier --write $(CURDIR)/**/*.md

rename: $(TARGET)
ifneq ($(and $(OS), $(ARCH)), )
	mv $< $(DIST)/$(NAME)-$(OS)-$(ARCH)$(EXE)
endif

$(BIN):
	mkdir --parents $@

ifeq ($(GITHUB_TOKEN),)
  SORT_GITHUB_OPTIONS :=
else
  SORT_GITHUB_OPTIONS := --token $(GITHUB_TOKEN)
endif
$(DOCS)/awesome-github.md: $(DATA)/github.yaml
	poetry run utils.py sort github $(SORT_GITHUB_OPTIONS) $< > $@
	prettier --write $@

$(DOCS)/index.md: $(CURDIR)/main.py
	typer $< utils docs --name $(NAME) --output $@
	prettier --write $@

$(TARGET):
	pyinstaller --distpath $(DIST) --workpath $(BUILD) --onefile --name $(NAME) $(CURDIR)/main.py
