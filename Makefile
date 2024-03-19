DEMO :=

default: docs

.PHONY: docs
docs: docs/data

.PHONY: docs/data
docs/data: docs/data/bgm.json
docs/data: docs/data/demo.json
docs/data: docs/data/github.json

ifeq ($(DEMO),)
docs/data/%.json: config/%.yaml
	@ mkdir --parents --verbose "$(@D)"
	rye run awesome mixed < "$<" > "$@"
else
docs/data/%.json: docs/data/demo.json
	@ mkdir --parents --verbose "$(@D)"
	@ cp --archive --no-target-directory --verbose "$<" "$@"
endif

docs/data/bgm.json:
	@ mkdir --parents --verbose "$(@D)"
	rye run awesome bgm > "$@"

docs/data/demo.json: config/demo.yaml
	@ mkdir --parents --verbose "$(@D)"
	rye run awesome mixed < "$<" > "$@"
