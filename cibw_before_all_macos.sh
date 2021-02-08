#!/bin/bash

set -e -x

brew install automake swig
uconv -V

source ./build_hfst.sh
