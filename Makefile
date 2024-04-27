default:

.PHONY: data
data:
	@ cp --recursive --verbose "data" "web"
	$(MAKE) --always-make web/data/bgm.json web/data/data.json

web/data/bgm.json:
	@ mkdir --parents --verbose "$(@D)"
	cd "python" && rye run awesome bgm > "$(abspath $@)"

web/data/data.json: web/data/items.txt
	@ mkdir --parents --verbose "$(@D)"
	cd "python" && rye run awesome item < "$(abspath $<)" > "$(abspath $@)"

web/data/items.txt:
	@ mkdir --parents --verbose "$(@D)"
	cd "web" && bun run build | grep "^{" > "$(abspath $@)"
