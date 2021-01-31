#!/bin/bash

set -e -x

# echo "STEP Cleaning old files..."
# yes | rm -fr _libhfst*.so build/ dist/ wheelhouse/

echo "STEP Configuring..."
cd hfst_src/
autoreconf -i  # Is this necessary?
./configure --enable-all-tools --with-readline --enable-fsmbook-tests
# make clean
make

echo "STEP Making flex/yacc files..."
cd libhfst/src/parsers/
make  # this is unnecessary if `make` is already called in the root dir, but it doesn't hurt
cd ../../../../

# TODO renaming *.cc to *.cpp in backends/ and libhfst/ might be necessary on Windows.
