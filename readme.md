# Agr

## Why

Repo wide search and replace should be easier.

## What

Like ack or ag, but for search and replace.

Can climb to the root of a git repo before running.

Shows a preview of the replacements to be made.

Prompts to continue globally or at each change site.

## Install

```bash
python3 -m pip install git+https://github.com/nathants/agr
```

## Usage

```bash
agr '(\w+)_factory' '\1_factory_factory'
```

## Dependencies
 - [Silver-search (ag)](https://github.com/ggreer/the_silver_searcher)
 - [Python3](https://python.org)

## Examples

```
$ agr '(\w+)_factory' '\1_factory_factory'
> lib.py:14: def poodle_factory_factory(): => def poodle_factory_factory_factory():
> main.py:3: def dog_factory_factory(): => def dog_factory_factory_factory():
> proceed? y/n
```

```
$ agr '(\w+)_factory' --delete
> lib.py:14: def poodle_factory_factory(): => DELETED!
> main.py:3: def dog_factory_factory(): => DELETED!
> proceed? y/n
```

```
>> agr -h
usage: agr [-h] [-d] [-p] [-s] [-u] [-n] [-y] [-e] pattern [replacement]

positional arguments:
  pattern             regex to match
  replacement         replacement for matches (default: -)

optional arguments:
  -h, --help          show this help message and exit
  -d, --delete        rather than substitute replacement, delete the matched line (default: False)
  -p, --preview       show diffs and then exit without prompting for commit (default: False)
  -s, --short         show shorter diffs (default: False)
  -u, --unrestricted  process all files, not just code files (default: False)
  -n, --no-climb      no climbing upwards until a .git dir is found (default: False)
  -y, --yes           commit without prompting (default: False)
  -e, --each          prompt for y/n at each change site (default: False)
```