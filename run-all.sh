#!/bin/bash
set -xeu

for d in */; do
    cd $d
    for f in *.py; do
        python3 $f
    done
    cd -
done
echo OK
