import argh
import itertools
import os
import pager
import re
import subprocess
import sys

red    = lambda x: "\033[31m%s\033[0m" % x
green  = lambda x: "\033[32m%s\033[0m" % x
yellow = lambda x: "\033[33m%s\033[0m" % x

@argh.arg('-p', '--preview')
def _main(pattern: 'regex to match',
          replacement: 'replacement for matches',
          preview: 'show diffs and then exit without prompting for commit' = False,
          short: 'show shorter diffs' = False,
          no_climb_git_root: 'dont cd upwards until a .git dir is found' = False,
          yes: 'commit without prompting' = False):
    """

    like ack or ag, but for search and replace. operates from the root
    of a git repo, and fails if not run within a git repo. shows a preview
    of the replacements to be made, and prompts to continue.

    $ agr '(\w+)_factory' '\1_factory_factory'

    $ agr -h

    """
    if not no_climb_git_root:
        while True:
            if os.getcwd() == '/':
                print('failed to find git root')
                sys.exit(1)
            if '.git' in os.listdir():
                break
            os.chdir('..')
    try:
        matches = [(path, num)
                   for line in subprocess.check_output(['ag', '-s', pattern]).decode('utf-8').strip().splitlines()
                   for path, num, _ in [line.split(':', 2)]]
    except subprocess.CalledProcessError:
        print('no matches')
        sys.exit(1)
    matches = sorted(matches, key=lambda x: x[0])
    matches = itertools.groupby(matches, key=lambda x: x[0])
    matches = [(path, [int(num) - 1
                       for _, num in nums
                       if num.isdigit()]) # paths with ":" in them a skipped
               for path, nums in matches]
    matches = [(path, nums) for path, nums in matches if nums]
    def update(path, nums):
        with open(path) as f:
            lines = f.read().splitlines()
        for num in nums:
            line = lines[num]
            assert re.search(pattern, line), 'python didnt find a match that ag found for %(path)s:%(num)s' % locals()
            pattern_no_split = re.sub(r'[\(\)]', '', pattern)
            unchanged = [x for x in re.split(pattern_no_split, line)]
            olds = re.findall(pattern_no_split, line)
            news = [re.sub(pattern, replacement, x) for x in olds]
            lines[num] = ''.join(sum(zip([''] + news, unchanged), ()))
            if short:
                print(yellow(path) + ':' + yellow(str(num)) + ': ' + ', '.join('%s => %s' % (red(old), green(new)) for old, new in zip(olds, news)))
            else:
                old = ''.join(sum(zip([''] + list(map(red, olds)), unchanged), ())).strip()
                new = ''.join(sum(zip([''] + list(map(green, news)), unchanged), ())).strip()
                print(yellow(path) + ':' + yellow(str(num)) + ': ' + '%(old)s => %(new)s' % locals())
        return lines
    updates = [(path, update(path, nums)) for path, nums in matches]
    if not preview:
        if not yes:
            print('proceed? y/n ')
            if pager.getch() != 'y':
                print('abort')
                sys.exit(1)
        for path, lines in updates:
            with open(path, 'w') as f:
                f.write('\n'.join(lines) + '\n')
            print('updated:', path)

def main():
    argh.dispatch_command(_main)
