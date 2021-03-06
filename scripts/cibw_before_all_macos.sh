#!/bin/bash

# This script is run by cibuildwheel in .github/actions/build.yml
# (specified under CIBW_BEFORE_ALL_MACOS)

set -e -x

brew install automake bison flex icu4c  # to build hfst from source
export PATH="/usr/local/opt/bison/bin:/usr/local/opt/flex/bin:$PATH"
export CPPFLAGS="-I/usr/local/opt/flex/include"
export LDFLAGS="-L/usr/local/opt/bison/lib -L/usr/local/opt/flex/lib"

brew install swig


# Download precompiled HFST binaries from Apertium
# mkdir tmp
# cd tmp
# curl https://apertium.projectjj.com/osx/nightly/hfst-latest.tar.bz2 > hfst-latest.tar.bz2
# tar -xzf hfst-latest.tar.bz2
# cd ..
# cp tmp/hfst/lib/libhfst.dylib hfst/lib/
# export LDFLAGS="-L$(pwd)/tmp/hfst/lib ${LDFLAGS}"

# export MACOSX_DEPLOYMENT_TARGET=10.9
echo "ENV DEBUG"
env

# Build ICU (brew has too recent MACOSX_DEPLOYMENT_TARGET)
# mkdir icu_tmp
# cd icu_tmp/
# wget https://github.com/unicode-org/icu/archive/release-68-2.tar.gz
# tar -xzf release-68-2.tar.gz
# cd icu-release-68-2/icu4c/source/
# ./runConfigureICU MacOSX/GCC
# make
# make install
# cd ../../../../

# Build HFST from source
echo "deployment target: ${MACOSX_DEPLOYMENT_TARGET}"
cd hfst_src/
autoreconf -fvi
./configure --disable-static  \
	    --enable-all-tools  \
	    --with-readline  \
	    --with-unicode-handler=icu  \
	    MACOSX_DEPLOYMENT_TARGET=10.9
make
make check V=1 VERBOSE=1
make install
cd ..

python setup.py build_ext
