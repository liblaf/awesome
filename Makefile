DEMO :=

default: docs

.PHONY: docs
docs: docs/data
docs: docs/docs

.PHONY: docs/data
docs/data: docs/data/bgm.json
docs/data: docs/data/demo.json
docs/data: docs/data/github.json

ifeq ($(DEMO),)
docs/data/github.json: $(wildcard config/*.yaml)
	@ mkdir --parents --verbose "$(@D)"
	cat $^ | rye run awesome mixed > "$@"
else
docs/data/github.json: docs/data/demo.json
	@ mkdir --parents --verbose "$(@D)"
	@ cp --archive --no-target-directory --verbose "$<" "$@"
endif

docs/data/bgm.json:
	@ mkdir --parents --verbose "$(@D)"
	rye run awesome bgm > "$@"

docs/data/demo.json: config/demo.yaml
	@ mkdir --parents --verbose "$(@D)"
	rye run awesome mixed < "$<" > "$@"

.PHONY: docs/docs
docs/docs: docs/docs/alternatives/cli.mdx docs/docs/github/github.mdx docs/docs/github/languages.mdx docs/docs/github/websites.mdx

docs/docs/alternatives/cli.mdx: config/alternatives.yaml
docs/docs/alternatives/cli.mdx: TITLE := CLI
docs/docs/github/github.mdx: config/github.yaml
docs/docs/github/github.mdx: TITLE := GitHub
docs/docs/github/languages.mdx: config/languages.yaml
docs/docs/github/languages.mdx: TITLE := Languages
docs/docs/github/websites.mdx: config/websites.yaml
docs/docs/github/websites.mdx: TITLE = Websites
docs/docs/alternatives/cli.mdx docs/docs/github/github.mdx docs/docs/github/languages.mdx docs/docs/github/websites.mdx:
	@ mkdir --parents --verbose "$(@D)"
	rye run awesome mdx "$(TITLE)" < "$<" > "$@"
	prettier --write "$@"
