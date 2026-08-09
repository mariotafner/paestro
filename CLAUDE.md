# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`paestro` is a Python utility library for the Maestro platform, distributed as a pip-installable package via GitHub. The package name (`paestro`) differs from the repo directory name (`maestro_py_utils`).

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package in editable mode (for local development)
pip install -e .

# Reinstall from GitHub (used by consumers of this library)
pip uninstall paestro -y && pip install --upgrade --no-cache-dir git+https://github.com/mariotafner/paestro.git

# Release a new version: bump version in pyproject.toml, then:
git tag <version>
git push --tags
```

There is no test runner — `test.py` is a scratch file for manual experimentation, not a test suite.

## Architecture

All library code lives in a single file: `paestro/utils.py`. The `Paestro` class is a flat collection of `@staticmethod` methods — there is no state, no subclasses, and no inheritance. `paestro/__init__.py` re-exports only `Paestro`.

Method categories in `Paestro`:
- **DateTime**: `datetime`, `dateCompare`, `dateAdd`, `secondsBetween`, `dateToJsDate`, `date_weekday`, `datetime_set_time`, `string_to_datetime`, `unitToSeconds`, `secondsToUnit`, `seconds_to_duration`
- **Strings/Random**: `random_id`, `random_string`, `random_int`, `random_choice`, `randomize_list`, `fill_zeros`, `split_chunks`, `string_pad_left`, `string_pad_right`, `remove_duplicated_spaces`, `msort`
- **File/Binary**: `file_to_base64`, `base64_to_file`, `base64_encode`, `base64_decode`, `gzip_compress`, `gzip_decompress`, `gzip_compress_bytes`, `gzip_decompress_bytes`, `save_file_bytes`, `read_file_bytes`, `listdir`, `reduce_jpeg_quality`
- **Network**: `get_ssl_info`, `get_url_base64`, `ssh_exec`, `ssh_send_file`, `ping`

`ssh_exec` returns `(result: str, lines: List[str], ms: float)` — stdout is preferred over stderr; trailing newline and blank lines are stripped.

`seconds_to_duration` returns Portuguese-language strings (e.g., `"2 dias e 3 horas"`).

`date_weekday` returns 1–7 (Monday–Sunday), not Python's 0–6.

## Adding New Utilities

Add new `@staticmethod` methods directly to the `Paestro` class in `paestro/utils.py`. After adding, bump `version` in `pyproject.toml` and tag the release.
