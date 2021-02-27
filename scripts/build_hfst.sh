#!/bin/bash

set -e -x

echo "deployment target: ${MACOSX_DEPLOYMENT_TARGET}"
cd hfst_src/
autoreconf -fvi
./configure --disable-static --enable-all-tools --with-readline --with-unicode-handler=glib
make
make check V=1 VERBOSE=1
make install
cd ..
