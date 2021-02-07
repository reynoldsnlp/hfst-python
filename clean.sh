#!/bin/bash

set -e -x

echo "Cleaning old files..."
# TODO are there others?
yes | rm -fr hfst/_libhfst*.so hfst/libhfst.py hfst/libhfst_wrap.cpp hfst/lib/*.dylib build/ dist/ wheelhouse/
