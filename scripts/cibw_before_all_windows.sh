#!/bin/bash

# This script is run by cibuildwheel in .github/actions/build.yml
# (specified under CIBW_BEFORE_ALL_WINDOWS)


set -e -x

# choco upgrade -y --no-progress winflexbison3 swig  # libicu-devel readline-devel
pacman -S --noconfirm --needed  \
           bison  \
           flex  \
           icu-devel  \
           swig


git clone https://github.com/dlfcn-win32/dlfcn-win32.git
cd dlfcn-win32/
./configure
make
make install
cd ..

export CPPFLAGS="-I/usr/include -I/mingw/include ${CPPFLAGS}"
export LDFLAGS="-L/usr/lib -L/mingw/lib ${LDFLAGS}"
export PATH="/usr/bin/:${PATH}"
export PKG_CONFIG_PATH="/usr/lib/pkgconfig:${PKG_CONFIG_PATH}"


#           base-devel  \
#           mingw-w64-i686-toolchain  \
#           mingw-w64-x86_64-toolchain  \
#           # mingw-w64-cross-toolchain  \
#           mingw-w64-x86_64-libtool  \
#           mingw-w64-x86_64-icu  \
#           glib2-devel  \
#           swig

cd libhfst_src/
autoreconf -fvi
./configure --enable-mingw --with-unicode-handler=icu
make
make check V=1 VERBOSE=1
make install
cd ..

python3 setup.py build_ext
