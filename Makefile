default: ruff stub

build: docs
	mkdocs build

.PHONY: docs
docs: docs/acg.md docs/alternatives.md docs/github.md docs/languages.md docs/websites.md

gh-deploy: docs
	mkdocs gh-deploy

ruff:
	ruff format
	ruff check --fix --unsafe-fixes

serve: docs
	mkdocs serve

setup:
	micromamba create --yes --name "awesome" python poetry
	micromamba run --name "awesome" poetry install

stub:
	stubgen --include-docstrings --output "." --package "awesome"
	$(MAKE) ruff
	stubtest "awesome"

###############
# Auxiliaries #
###############

docs/acg.md:
	awesome bangumi > "$@"

docs/alternatives.md: data/alternatives.yaml
docs/alternatives.md: TITLE := Alternatives
docs/github.md: data/github.yaml
docs/github.md: TITLE := GitHub
docs/languages.md: data/languages.yaml
docs/languages.md: TITLE := Languages
docs/websites.md: data/websites.yaml
docs/websites.md: TITLE := Websites
docs/github.md docs/languages.md docs/websites.md:
	awesome mixed --title "$(TITLE)" "$<" > "$@"
