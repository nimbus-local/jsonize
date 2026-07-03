# jsonize

## What this is

A single-file Python 3 CLI that turns shell arguments into JSON. `jsonize
key=value ...` produces a JSON object; an array mode produces a JSON array
from bare values. No dependencies beyond the Python 3 standard library.
Requires Python 3.14+ (enforced by a version guard at the top of the script
and `requires-python` in pyproject.toml — keep the two in sync).

## Dependency policy

Stdlib only — `json`, `sys`, `base64`, `re`, `argparse`. Do not add
third-party packages (including for testing) without discussing it first;
this project's whole value proposition is "no dependencies to trust."

## Structure

Keep it a single file (`jsonize.py` or similar) for as long as reasonably
possible. If it grows enough to need splitting, keep the split minimal and
justified rather than pre-emptively modularizing.

## Install / run

Two supported paths, both dependency-free:

1. Shebang + `chmod +x` — run it directly off `$PATH`, no build step.
2. `pyproject.toml` with a `[project.scripts]` entry point, installed via
   `pip install .` (or from PyPI once published) — gives a `jsonize`
   executable on `PATH`.

Do not add binary-compilation tooling (PyInstaller, etc.) — it pulls in
third-party build tooling for no real benefit over the two paths above.

## Testing

Use the stdlib `unittest` module (no `pytest` or other test-runner
dependency) so the project stays install-free for contributors and CI
alike.

## License

MIT.
