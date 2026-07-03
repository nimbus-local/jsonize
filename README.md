# jsonize

Build JSON objects and arrays from shell arguments, using nothing but the Python 3 standard library.

```bash
$ jsonize name=jsonize count=17 stable=false
{"name": "jsonize", "count": 17, "stable": false}
```

## Status

Early development. Core object/array construction is being built out; nested
key paths, type-coercion overrides, and file-based value substitution are
planned next.

## Requirements

Python 3, no third-party dependencies.
