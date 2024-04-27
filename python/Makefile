default: fmt

fmt: fmt-toml/pyproject.toml

fmt-toml/%:
	toml-sort --in-place --all "$*"
	taplo format "$*"
