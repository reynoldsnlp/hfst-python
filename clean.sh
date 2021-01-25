#!/bin/bash

set -e -x

echo "Cleaning old files..."
# TODO are there others?
yes | rm -fr _libhfst*.so build/ dist/ wheelhouse/
