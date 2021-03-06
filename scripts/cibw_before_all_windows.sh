#!/bin/bash

# This script is run by cibuildwheel in .github/actions/build.yml
# (specified under CIBW_BEFORE_ALL_WINDOWS)


set -e -x

# choco upgrade -y --no-progress winflexbison3 swig  # libicu-devel readline-devel
pacman -S --noconfirm --needed  \
           bison  \
           flex  \
           icu-devel

export CPPFLAGS="-I/c/msys2/usr/include ${CPPFLAGS}"
export LDFLAGS="-L/c/msys2/usr/lib ${LDFLAGS}"
export PATH="/c/msys2/usr/bin/:${PATH}"
export PKG_CONFIG_PATH="/c/msys2/usr/lib/pkgconfig:${PKG_CONFIG_PATH}"


#           base-devel  \
#           mingw-w64-i686-toolchain  \
#           mingw-w64-x86_64-toolchain  \
#           # mingw-w64-cross-toolchain  \
#           mingw-w64-x86_64-libtool  \
#           mingw-w64-x86_64-icu  \
#           glib2-devel  \
#           swig

cd hfst_src/
autoreconf -fvi
./configure --with-unicode-handler=icu
make
make check V=1 VERBOSE=1
make install
cd ..

python setup.py build_ext
