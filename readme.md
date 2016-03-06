like ack or ag, but for search and replace. operates from the root
of a git repo, and fails if not run within a git repo. shows a preview
of the replacements to be made, and prompts to continue.

installation: `pip3 install https://github.com/nathants/agr`
alternate installation: `git clone https://github.com/nathants/agr && cd agr && python3 setup.py install`

usage: `agr '(\w+)_factory' '\1_factory_factory'`

usage: `agr -h`

notes:
 - depends on [silver-search (ag)](https://github.com/ggreer/the_silver_searcher) being available.
 - depends on python3.4+, but probably works with other pythons with or without minor modifications.
 - diffs are colorized for ease of reading.

examples:

```
$ agr '(\w+)_factory' '\1_factory_factory'
> lib.py:14: def poodle_factory_factory(): => def poodle_factory_factory_factory():
> main.py:3: def dog_factory_factory(): => def dog_factory_factory_factory():
> proceed? y/n
> updated: lib.py
> updated: main.py
```

```
$ agr '(\w+)_factory' '\1_factory_factory' --short
> lib.py:14: poodle_factory => poodle_factory_factory
> main.py:3: dog_factory => dog_factory_factory
> proceed? y/n
> updated: lib.py
> updated: main.py
```

```
$ agr -h
> usage: agr [-h] [-p] [-s] [-y] [-n] pattern replacement
>
> positional arguments:
>   pattern        regex to match
>   replacement    replacement for matches
>
> optional arguments:
>   -h, --help     show this help message and exit
>   -p, --preview  show diffs and then exit without prompting for commit (default: False)
>   -s, --short    show shorter diffs (default: False)
>   -y, --yes      commit with prompting (default: False)
```
