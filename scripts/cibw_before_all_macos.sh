#!/bin/bash

# This script is run by cibuildwheel in .github/actions/build.yml
# (specified under CIBW_BEFORE_ALL_MACOS)

set -e -x

brew install automake bison flex  # to build hfst from source
export PATH="/usr/local/opt/bison/bin:/usr/local/opt/flex/bin:$PATH"
export CPPFLAGS="-I/usr/local/opt/flex/include -I/usr/local/include/unicode"  # -I/usr/local/opt/icu4c/include"
export LDFLAGS="-L/usr/local/opt/bison/lib -L/usr/local/opt/flex/lib -L/usr/local/lib"  # -L/usr/local/opt/icu4c/lib"
# export PKG_CONFIG_PATH="/usr/local/opt/icu4c/lib/pkgconfig"
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig"

# brew install swig


# Download precompiled HFST binaries from Apertium
# mkdir tmp
# cd tmp
# curl https://apertium.projectjj.com/osx/nightly/hfst-latest.tar.bz2 > hfst-latest.tar.bz2
# tar -xzf hfst-latest.tar.bz2
# cd ..
# cp tmp/hfst/lib/libhfst.dylib hfst/lib/
# export LDFLAGS="-L$(pwd)/tmp/hfst/lib ${LDFLAGS}"

# Build ICU (brew has too recent MACOSX_DEPLOYMENT_TARGET)
brew uninstall --ignore-dependencies icu4c
mkdir icu_tmp
cd icu_tmp/
wget https://github.com/unicode-org/icu/archive/release-68-2.tar.gz
tar -xzf release-68-2.tar.gz
cd icu-release-68-2/icu4c/source/
./runConfigureICU MacOSX/GCC
make
make install
cd ../../../../
cp /usr/local/lib/libicu* .  # TODO For some reason `delocate` looks here for dylibs

# Build HFST from source
echo "deployment target: ${MACOSX_DEPLOYMENT_TARGET}"
cd libhfst_src/
autoreconf -fvi
./configure --with-unicode-handler=icu
make -C back-ends
make -C libhfst
cd ..

python setup.py sdist
