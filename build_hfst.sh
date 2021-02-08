#!/bin/bash

set -e -x

cd hfst_src/
autoreconf -fvi
./configure --disable-static --enable-all-tools --with-readline --with-unicode-handler=icu
make
make check V=1 VERBOSE=1
make install
cd ..
