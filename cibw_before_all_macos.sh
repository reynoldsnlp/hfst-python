#!/bin/bash

set -e -x

brew install autoconf automake bison flex icu4c libtool readline swig

source ./build_hfst.sh
