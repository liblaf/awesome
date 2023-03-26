# `utils.py`

**Usage**:

```console
$ utils.py [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--help`: Show this message and exit.

**Commands**:

- `hello`
- `sort`

## `utils.py hello`

**Usage**:

```console
$ utils.py hello [OPTIONS] [NAME] COMMAND [ARGS]...
```

**Arguments**:

- `[NAME]`: [default: world]

**Options**:

- `--help`: Show this message and exit.

## `utils.py sort`

**Usage**:

```console
$ utils.py sort [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--help`: Show this message and exit.

**Commands**:

- `github`: Examples: $ utils.py sort github...
- `json`
- `url`: Examples: $ utils.py sort github...
- `yaml`

### `utils.py sort github`

Examples:
$ utils.py sort github data/github.yaml > docs/awesome-github.md

**Usage**:

```console
$ utils.py sort github [OPTIONS] [FILEPATH] COMMAND [ARGS]...
```

**Arguments**:

- `[FILEPATH]`

**Options**:

- `-t, --token TEXT`
- `--help`: Show this message and exit.

### `utils.py sort json`

**Usage**:

```console
$ utils.py sort json [OPTIONS] FILEPATH COMMAND [ARGS]...
```

**Arguments**:

- `FILEPATH`: [required]

**Options**:

- `--help`: Show this message and exit.

### `utils.py sort url`

Examples:
$ utils.py sort github data/github.yaml > docs/awesome-github.md

**Usage**:

```console
$ utils.py sort url [OPTIONS] [FILEPATH] COMMAND [ARGS]...
```

**Arguments**:

- `[FILEPATH]`

**Options**:

- `--help`: Show this message and exit.

### `utils.py sort yaml`

**Usage**:

```console
$ utils.py sort yaml [OPTIONS] FILEPATH COMMAND [ARGS]...
```

**Arguments**:

- `FILEPATH`: [required]

**Options**:

- `--help`: Show this message and exit.
