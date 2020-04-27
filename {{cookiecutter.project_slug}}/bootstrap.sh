#!/bin/bash

log() {
  level=$1
  message=$2
  echo "`hostname` `date +'%Y-%m-%d %H:%M:%S'` $1 $2"
}

MODE="$1"

if [ -z $1 ]; then
  echo "usage: ./bootstrap.sh dev|prod"
  exit 1
fi

if [ ! -d ".venv" ]; then
  log INFO "setup .venv begin ..."
  python3 -m venv .venv
  source .venv/bin/activate
  pip install wheel
  pip install -r ./requirements/$MODE.txt
  log INFO "setup .venv end"
fi

# if [ ! -d "{{ cookiecutter.pkg_name }}/static/upload" ]; then
#   log INFO "mkdir upload begin ..."
#   mkdir -p {{ cookiecutter.pkg_name }}/static/upload/file
#   mkdir -p {{ cookiecutter.pkg_name }}/static/upload/img
#   log INFO "mkdir upload end"
# fi

exit 0
