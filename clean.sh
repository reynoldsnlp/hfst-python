#!/bin/bash

set -e -x

echo "Cleaning old files..."
# TODO are there others?
yes | rm -fr _libhfst*.so hfst/lib/*.dylib hfst/libhfst_wrap.cpp hfst/libhfst.py build/ dist/ wheelhouse/
