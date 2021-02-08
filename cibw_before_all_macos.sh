#!/bin/bash

set -e -x

brew install autoconf automake swig bison flex readline libtool

source ./build_hfst.sh
