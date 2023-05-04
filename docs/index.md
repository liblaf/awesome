# `utils`

**Usage**:

```console
$ utils [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `hello`
- `nginx`
- `sort`

## `utils hello`

**Usage**:

```console
$ utils hello [OPTIONS]
```

**Options**:

- `-n, --name TEXT`: [default: world]
- `--help`: Show this message and exit.

## `utils nginx`

**Usage**:

```console
$ utils nginx [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--help`: Show this message and exit.

**Commands**:

- `add`
- `disable`
- `enable`
- `list`

### `utils nginx add`

**Usage**:

```console
$ utils nginx add [OPTIONS] DOMAIN
```

**Arguments**:

- `DOMAIN`: [required]

**Options**:

- `--port INTEGER`: [default: 8000]
- `--nginx-dir DIRECTORY`: [default: /etc/nginx]
- `--help`: Show this message and exit.

### `utils nginx disable`

**Usage**:

```console
$ utils nginx disable [OPTIONS] DOMAIN
```

**Arguments**:

- `DOMAIN`: [required]

**Options**:

- `-d, --nginx-dir DIRECTORY`: [default: /etc/nginx]
- `--help`: Show this message and exit.

### `utils nginx enable`

**Usage**:

```console
$ utils nginx enable [OPTIONS] DOMAIN
```

**Arguments**:

- `DOMAIN`: [required]

**Options**:

- `-d, --nginx-dir DIRECTORY`: [default: /etc/nginx]
- `--help`: Show this message and exit.

### `utils nginx list`

**Usage**:

```console
$ utils nginx list [OPTIONS]
```

**Options**:

- `-d, --nginx-dir DIRECTORY`: [default: /etc/nginx]
- `--help`: Show this message and exit.

## `utils sort`

**Usage**:

```console
$ utils sort [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `--help`: Show this message and exit.

**Commands**:

- `github`
- `website`

### `utils sort github`

**Usage**:

```console
$ utils sort github [OPTIONS] DATA_FILEPATH
```

**Arguments**:

- `DATA_FILEPATH`: [required]

**Options**:

- `-i, --in-place`
- `-m, --markdown FILE`
- `-t, --token TEXT`: [env var: GITHUB_TOKEN]
- `--help`: Show this message and exit.

### `utils sort website`

**Usage**:

```console
$ utils sort website [OPTIONS] DATA_FILEPATH
```

**Arguments**:

- `DATA_FILEPATH`: [required]

**Options**:

- `-i, --in-place`
- `-m, --markdown FILE`
- `--help`: Show this message and exit.
