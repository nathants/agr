#!/bin/bash
#
# like ack or ag, but for search and replace. operates from the root
# of a git repo, and fails if not run within a git repo. shows a preview
# of the replacements to be made, and prompts to continue.
#
# $ agr '(\w+)_factory' '\1_factory_factory' [yes|no]
#
# the third argument, when yes, commits with prompting, when no, exits
# without prompting to commit, and when absent, prompts before committing.
#
# depends on silver-searcher (ag) and sed.
#

set -e

while true; do
    [ $(pwd) = "/" ] && echo failed to find git root && exit 1
    ls .git >/dev/null 2>&1 && break || cd ..
done

pattern=$1
replacement=$2
doit=$3
matches=$(ag -s ${pattern})

echo "${matches}" | while read name; do
    path=$(echo $name|cut -d: -f1)
    num=$(echo $name|cut -d: -f2)
    echo ${path}:${num} $(sed -n "${num}p" "${path}") '=>' $(sed -r "${num}s:${pattern}:${replacement}:g" "$path")
done

if [ "${doit}" = "no" ]; then
    proceed=n
elif [ "${doit}" = "yes" ]; then
    proceed=y
else
    echo proceed? y/n
    read -n1 proceed
    echo ""
fi

if [ "${proceed}" = "y" ]; then
    echo "${matches}" | while read name; do
        path=$(echo $name|cut -d: -f1)
        num=$(echo $name|cut -d: -f2)
        sed -i -r "${num}s:${pattern}:${replacement}:" "${path}"
        echo updated: ${path}
    done
else
    echo abort
    exit 1
fi
