#!/bin/bash

set -e -x

# TODO not everything needs to be compiled. Limit make targets accordingly

cd hfst_src/
git pull
autoreconf -i  # Is this necessary?
./configure --enable-all-tools --with-readline --enable-fsmbook-tests
# make clean
make
cd ..
