DEMO :=

default: docs

.PHONY: docs
docs: docs/data
docs: docs/docs

.PHONY: docs/data
docs/data: docs/data/bgm.json
docs/data: docs/data/demo.json
docs/data: docs/data/awesome.json

ifeq ($(DEMO),)
docs/data/awesome.json: $(wildcard config/*.yaml)
	@ mkdir --parents --verbose "$(@D)"
	cat $^ | rye run awesome mixed > "$@"
else
docs/data/awesome.json: docs/data/demo.json
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
docs/docs: docs/docs/alternatives/cli.mdx docs/docs/awesome/github.mdx docs/docs/awesome/languages.mdx docs/docs/awesome/websites.mdx

docs/docs/alternatives/cli.mdx: config/alternatives.yaml
docs/docs/alternatives/cli.mdx: TITLE := CLI
docs/docs/awesome/github.mdx: config/github.yaml
docs/docs/awesome/github.mdx: TITLE := GitHub
docs/docs/awesome/languages.mdx: config/languages.yaml
docs/docs/awesome/languages.mdx: TITLE := Languages
docs/docs/awesome/websites.mdx: config/websites.yaml
docs/docs/awesome/websites.mdx: TITLE = Websites
docs/docs/alternatives/cli.mdx docs/docs/awesome/github.mdx docs/docs/awesome/languages.mdx docs/docs/awesome/websites.mdx:
	@ mkdir --parents --verbose "$(@D)"
	rye run awesome mdx "$(TITLE)" < "$<" > "$@"
	prettier --write "$@"
