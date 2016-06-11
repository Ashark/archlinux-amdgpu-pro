#!/bin/sh
set -e
ROOT=$(cd $(dirname $0); pwd -P)

for hook in $ROOT/git/hooks/*
do
  hookName=$(basename $hook)
  echo "Installing $hookName..."
  ln -s -f -r $hook $ROOT/.git/hooks/$hookName
done
