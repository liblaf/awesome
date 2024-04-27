default:

data: web/data/bgm.json web/data/data.json

web/data/bgm.json:
	cd "python" && rye run awesome bgm > "$(abspath $@)"

web/data/data.json: web/data/items.txt
	cd "python" && rye run awesome item < "$(abspath $<)" > "$(abspath $@)"

web/data/items.txt:
	cd "web" && bun run build | grep "^{" > "$(abspath $@)"
