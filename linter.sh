#!/bin/bash
set -xeu

FLAGS="--disable=C,R"

if [ $# -ge 1 ]; then
    pylint $FLAGS "$@"
else
    pylint $FLAGS $(dirname $0)/*/*.py
fi
