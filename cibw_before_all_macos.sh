#!/bin/bash

set -e -x

# brew install bison flex  # to build from source, add to LDFLAGS and CPPFLAGS
brew install swig

mkdir tmp
cd tmp
curl https://apertium.projectjj.com/osx/nightly/hfst-latest.tar.bz2 > hfst-latest.tar.bz2
tar -xzf hfst-latest.tar.bz2
cd ..

cp tmp/hfst/lib/libhfst.dylib hfst/lib/
echo ${LDFLAGS}
export LDFLAGS="-L$(pwd)/tmp/hfst/lib"
