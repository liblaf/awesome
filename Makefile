default: docs

.PHONY: docs
docs: docs/data

.PHONY: docs/data
docs/data: docs/data/bgm.json

docs/data/bgm.json:
	@ mkdir --parents --verbose "$(@D)"
	rye run awesome bgm > "$@"
