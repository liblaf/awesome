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

AWESOME_LIST := docs/docs/alternatives/cli.mdx
AWESOME_LIST += docs/docs/alternatives/desktop.mdx
AWESOME_LIST += docs/docs/awesome/github.mdx
AWESOME_LIST += docs/docs/awesome/languages.mdx
AWESOME_LIST += docs/docs/awesome/websites.mdx
.PHONY: docs/docs
docs/docs: $(AWESOME_LIST)

docs/docs/alternatives/cli.mdx: config/alternatives/cli.yaml
docs/docs/alternatives/cli.mdx: TITLE := CLI
docs/docs/alternatives/desktop.mdx: config/alternatives/desktop.yaml
docs/docs/alternatives/desktop.mdx: TITLE := Desktop
docs/docs/awesome/github.mdx: config/github.yaml
docs/docs/awesome/github.mdx: TITLE := GitHub
docs/docs/awesome/languages.mdx: config/languages.yaml
docs/docs/awesome/languages.mdx: TITLE := Languages
docs/docs/awesome/websites.mdx: config/websites.yaml
docs/docs/awesome/websites.mdx: TITLE = Websites
$(AWESOME_LIST):
	@ mkdir --parents --verbose "$(@D)"
	rye run awesome mdx "$(TITLE)" < "$<" > "$@"
	prettier --write "$@"
