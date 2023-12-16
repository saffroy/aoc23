#!/bin/bash
set -xeu

BASE="$(dirname $0)"
PATH="$BASE/venv/bin/:$PATH"
FLAGS="--disable=C,R"

if [ $# -ge 1 ]; then
    pylint $FLAGS "$@"
else
    pylint $FLAGS "$BASE"/*/*.py
fi
