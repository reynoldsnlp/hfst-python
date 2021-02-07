#!/bin/bash

set -e -x

echo "Cleaning old files..."
# TODO are there others?
yes | rm -fr _libhfst*.so hfst/lib/libhfst.dylib hfst/libhfst_wrapper.cpp hfst/libhfst.py build/ dist/ wheelhouse/
