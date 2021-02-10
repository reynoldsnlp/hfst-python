#!/bin/bash

set -e -x

brew install automake bison flex swig
export PATH="/usr/local/opt/bison/bin:/usr/local/opt/flex/bin:$PATH"
export CPPFLAGS="-I/usr/local/opt/flex/include"
export LDFLAGS="-L/usr/local/opt/bison/lib -L/usr/local/opt/flex/lib"

source ./build_hfst.sh
