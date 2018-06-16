##### agr

like ack or ag, but for search and replace. can climb to the root of a
git repo before running. shows a preview of the replacements to be
made, and prompts to continue globally or at each change site.

installation methods:
 - `pip3 install https://github.com/nathants/agr@ab822da`
 - `git clone https://github.com/nathants/agr && cd agr && python3.6 setup.py develop`

usage: `agr '(\w+)_factory' '\1_factory_factory'`

usage: `agr -h`

depends on:
 - [silver-search (ag)](https://github.com/ggreer/the_silver_searcher) being available.
 - python3.6+

examples:

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
  -n, --no-climb      dont cd upwards until a .git dir is found (default: False)
  -y, --yes           commit without prompting (default: False)
  -e, --each          prompt for y/n at each change site (default: False)
```
