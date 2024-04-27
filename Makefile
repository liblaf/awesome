default:

data: web/data/data.json

web/data/data.json: web/data/items.txt
	cd "python" && rye run awesome < "$(abspath $<)" > "$(abspath $@)"

web/data/items.txt:
	cd "web" && bun run build | grep "^{" > "$(abspath $@)"
