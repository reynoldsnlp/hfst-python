#!/bin/bash

set -e -x

brew install automake bison flex swig

source ./build_hfst.sh
