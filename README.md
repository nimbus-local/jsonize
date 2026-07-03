# jsonize

Build JSON objects and arrays from shell arguments, using nothing but the
Python 3 standard library. A single file, no third-party dependencies,
works the same on macOS and Linux.

```bash
$ jsonize name=jsonize count=17 stable=false
{"name":"jsonize","count":17,"stable":false}
```

## Usage

```bash
jsonize [-apBDen] [-d keydelim] [-f file] [--] [[-s|-n|-b] word ...]
```

Object mode (default) takes `key=value` words and builds a JSON object.
Values are type-guessed: numbers and `true`/`false`/`null` are recognized,
everything else is a string.

```bash
$ jsonize tst=1457081292 lat=12.3456 name="JP Mens" nada=
{"tst":1457081292,"lat":12.3456,"name":"JP Mens","nada":null}
```

`key@value` builds a boolean (truthy if the value starts with `T`/`t`, or is
a number greater than zero):

```bash
$ jsonize switch=true morning@0
{"switch":true,"morning":false}
```

### Array mode

```bash
$ jsonize -a 1 2 3
[1,2,3]
$ seq 1 5 | jsonize -a
[1,2,3,4,5]
```

### Nesting

Bracket paths build nested objects/arrays directly:

```bash
$ jsonize -p name=Jane 'point[]=1' 'point[]=2' 'geo[lat]=10' 'geo[lon]=20'
{
  "name": "Jane",
  "point": [
    1,
    2
  ],
  "geo": {
    "lat": 10,
    "lon": 20
  }
}
```

`-d <delim>` lets you use a delimiter (e.g. a dot) instead of brackets for
object paths:

```bash
$ jsonize -d. geo.lat=10 geo.lon=20
{"geo":{"lat":10,"lon":20}}
```

Nested `jsonize` invocations compose naturally, since a value that parses as
JSON is embedded as-is:

```bash
$ jsonize name=JP object="$(jsonize fruit="Blood Orange" number=17)"
{"name":"JP","object":{"fruit":"Blood Orange","number":17}}
```

### Type coercion overrides

Prefix a word with `-s`, `-n`, or `-b` (after a `--`) to force it to
string/number/boolean, overriding the default type guess:

```bash
$ jsonize -- -s a=true b=true -n c="a string"
{"a":"true","b":true,"c":8}
```

### Reading/writing values from files

```bash
jsonize content=@path/to/file      # inline raw file contents
jsonize content=%path/to/file      # base64-encode file contents
jsonize nested=:path/to/file.json  # parse file contents as JSON
jsonize key:=path/to/file.json     # same, at the key level (works with -f too)
```

Prefix the special characters `@`, `%`, `:` with a backslash to treat them
as literal characters instead.

### Merging into existing JSON

```bash
jsonize -f existing.json newkey=value   # load existing.json, apply edits, print
jsonize -f - newkey=value               # read existing JSON from stdin instead
```

### Other flags

- `-p` pretty-print (default is compact, no whitespace)
- `-B` disable `true`/`false`/`null` literal recognition (treat as strings)
- `-D` deduplicate object keys (last value wins); default keeps duplicates
- `-n` skip keys whose value is empty, instead of emitting `null`
- `-e` produce no output at all when stdin is empty (instead of `{}` / `[]`)
- `-v` / `-V` print version (plain / as JSON)

## Install

Two dependency-free options:

```bash
./install.sh          # copies jsonize to ~/.local/bin and adds it to PATH
```

```bash
pip install .          # installs the jsonize script into your environment
```

## Requirements

Python 3.14+, no third-party dependencies.

## Testing

```bash
python3 -m unittest tests/test_jsonize.py
```
