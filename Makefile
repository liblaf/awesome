NAME := awesome

BUILD := $(CURDIR)/build
DATA  := $(CURDIR)/data
DIST  := $(CURDIR)/dist
DOCS  := $(CURDIR)/docs
SITE  := $(CURDIR)/site

SYSTEM  != python -c 'import platform; print(platform.system().lower())'
MACHINE != python -c 'import platform; print(platform.machine().lower())'
ifeq ($(SYSTEM), windows)
  EXE := .exe
else
  EXE :=
endif
DIST_TARGET := $(DIST)/$(NAME)-$(SYSTEM)-$(MACHINE)$(EXE)

DOCS_LIST += $(DOCS)/github.md
DOCS_LIST += $(DOCS)/index.md
DOCS_LIST += $(DOCS)/websites.md

all:

clean:
	@ find $(CURDIR) -type d -name '__pycache__' -exec $(RM) --recursive --verbose '{}' +
	@ find $(CURDIR) -type d -name '.cache'      -exec $(RM) --recursive --verbose '{}' +
	@ find $(CURDIR) -type f -name '*.spec'      -exec $(RM) --verbose '{}' +
	$(RM) --recursive $(BUILD)
	$(RM) --recursive $(DIST)
	$(RM) --recursive $(SITE)

dist: $(DIST_TARGET)

docs: $(DOCS_LIST)
	$(MAKE) pretty

docs-serve: docs
	mkdocs serve

pretty: black prettier

setup: $(DOCS)/requirements.txt
	poetry install
	conda install --yes libpython-static
	pip install --requirement=$<

#####################
# Auxiliary targets #
#####################

$(DIST_TARGET): $(CURDIR)/main.py
ifeq ($(SYSTEM), windows)
	pyinstaller --distpath=$(@D) --workpath=$(BUILD) --onefile --name=$(NAME)-$(SYSTEM)-$(MACHINE) $<
else
	python -m nuitka --standalone --onefile --output-filename=$(@F) --output-dir=$(@D) --remove-output $<
endif

$(DOCS)/github.md: $(DATA)/github.yaml
ifeq ($(GITHUB_TOKEN), )
	poetry run $(NAME) github --in-place --markdown=$@ $<
else
	poetry run $(NAME) github --in-place --markdown=$@ --token=$(GITHUB_TOKEN) $<
endif

$(DOCS)/index.md: $(CURDIR)/main.py
	typer $< utils docs --name=$(NAME) --output=$@

$(DOCS)/websites.md: $(DATA)/websites.yaml
	poetry run $(NAME) website --in-place --markdown=$@ $<

black:
	isort --profile black $(CURDIR)
	black $(CURDIR)

prettier: $(CURDIR)/.gitignore
	prettier --write --ignore-path=$< $(CURDIR)
