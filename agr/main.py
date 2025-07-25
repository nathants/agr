#!/usr/bin/env python3
# search and replace tool that climbs to git root and shows preview before applying changes
import signal
import argh
import itertools
import os
import re
import subprocess
import sys
import termios
import tty

red    = lambda x: f'\033[31m{x}\033[0m'
green  = lambda x: f'\033[32m{x}\033[0m'
yellow = lambda x: f'\033[33m{x}\033[0m'

class _deleted:
    __str__ = lambda _: 'DELETED!'
deleted = _deleted()

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        val = sys.stdin.read(1).lower()
        if val == '\x03':
            sys.exit(1)
        else:
            return val
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def prompt_proceed():
    print('prompt_proceed? y/n/q', file=sys.stderr, end=' ', flush=True)
    char = getch()
    print(char, file=sys.stderr)
    if char == 'q':
        os.kill(os.getpid(), signal.SIGTERM)
    elif char != 'y':
        print('abort', file=sys.stderr)
        sys.exit(1)

@argh.arg('-p', '--preview')
@argh.arg('replacement', nargs='?')
def agr(pattern: 'regex to match',
        replacement: 'replacement for matches',
        delete: 'rather than substitute replacement, delete the matched line' = False,
        preview: 'show diffs and then exit without prompting for commit' = False,
        short: 'show shorter diffs' = False,
        unrestricted: 'process all files, not just code files' = False,
        no_climb: 'no climbing upwards until a .git dir is found' = False,
        yes: 'commit without prompting' = False,
        each: 'prompt for y/n at each change site' = False):
    """
    like ack or ag, but for search and replace. can climb to the root of a
    git repo before running. shows a preview of the replacements to be
    made, and prompts to continue globally or at each change site.

    >> agr '(\\w+)_factory' '\\1_factory_factory'
    """
    if not (replacement is not None or delete):
        print('error: must use [replacement] or --delete, see: agr --help ', file=sys.stderr)
        sys.exit(1)
    if replacement is not None and delete:
        print('error: can only use one of [replacement] or --delete, see: agr --help ', file=sys.stderr)
        sys.exit(1)
    if not no_climb:
        while True:
            if os.getcwd() == '/':
                print('failed to find git root', file=sys.stderr)
                sys.exit(1)
            if '.git' in os.listdir():
                break
            os.chdir('..')
    split = re.compile(r':(\d+):').split
    try:
        matches = [(path, num)
                   for line in subprocess.check_output(['ag', '--ignore', '*.js.map'] + (['-u'] if unrestricted else []) + ['-s', pattern]).decode('utf-8').strip().splitlines()
                   if len(split(line, 1)) == 3
                   for path, num, _ in [split(line, 1)]]
    except subprocess.CalledProcessError:
        print('no matches', file=sys.stderr)
        sys.exit(1)
    matches = sorted(matches, key=lambda x: x[0])
    matches = itertools.groupby(matches, key=lambda x: x[0])
    matches = [(path, {int(num) - 1
                       for _, num in nums
                       if num.isdigit()})
               for path, nums in matches]
    matches = [(path, nums) for path, nums in matches if nums]
    def update(path, nums):
        with open(path) as f:
            for num, line in enumerate(f):
                if num not in nums:
                    yield line
                else:
                    if not re.search(pattern, line):
                        print(f'python didnt find a match that ag found for {path}:{num}', file=sys.stderr)
                    pattern_no_split = re.sub(r'(?<!\\)[\(\)]', '', pattern)
                    unchanged = [x for x in re.split(pattern_no_split, line)]
                    olds = re.findall(pattern_no_split, line)
                    if replacement is not None:
                        news = [re.sub(pattern, replacement, x) for x in olds]
                    elif delete:
                        news = [deleted]
                    if each:
                        vals = []
                        for i, (old, new) in enumerate(zip(olds, news)):
                            _olds = olds.copy()
                            _olds[i] = red(old)
                            _news = olds.copy()
                            _news[i] = green(new)
                            old_line = ''.join(sum(zip([''] + list(_olds), unchanged), ())).strip()
                            new_line = ''.join(sum(zip([''] + list(_news), unchanged), ())).strip()
                            print(f'{yellow(path)}:{yellow(str(num + 1))}: {old_line} => {new_line}')
                            try:
                                prompt_proceed()
                                vals.append(new)
                            except SystemExit:
                                vals.append(old)
                        yield ''.join(sum(zip([''] + vals, unchanged), ()))
                    else:
                        if short:
                            print(f'{yellow(path)}:{yellow(str(num))}:', end=' ')
                            print(', '.join(f'{red(old_line)} => {green(new_line)}' for old_line, new_line in zip(olds, news)))
                        else:
                            old_line = ''.join(sum(zip([''] + list(map(red, olds)), unchanged), ())).strip()
                            if news == [deleted]:
                                unchanged = ['' for _ in unchanged]
                            new_line = ''.join(sum(zip([''] + list(map(green, news)), unchanged), ())).strip()
                            print(f'{yellow(path)}:{yellow(str(num + 1))}: {old_line} => {new_line}')
                        if replacement is not None:
                            yield ''.join(sum(zip([''] + news, unchanged), ()))
                        elif delete:
                            pass
    updates = [[path, list(update(path, nums))] for path, nums in matches]
    if not preview:
        if not yes and not each:
            prompt_proceed()
        for path, lines in updates:
            with open(path, 'w') as f:
                f.write(''.join(lines))
            print('updated:', path, file=sys.stderr)

def main():
    argh.dispatch_command(agr)

if __name__ == '__main__':
    main()
