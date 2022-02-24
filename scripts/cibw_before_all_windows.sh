#!/bin/bash

# This script is run by cibuildwheel in .github/actions/build.yml
# (specified under CIBW_BEFORE_ALL_WINDOWS)


set -e -x

# choco upgrade -y --no-progress winflexbison3 swig  # libicu-devel readline-devel
pacman -S --noconfirm --needed  \
           bison  \
           mingw-w64-i686-autotools  \
           mingw-w64-i686-dlfcn  \
           mingw-w64-i686-flexdll  \
           mingw-w64-i686-gettext  \
           mingw-w64-i686-icu  \
           mingw-w64-x86_64-autotools  \
           mingw-w64-x86_64-dlfcn  \
           mingw-w64-x86_64-flexdll  \
           mingw-w64-x86_64-gettext  \
           mingw-w64-x86_64-icu
           # autotools  \
           # flex  \
           # icu-devel  \

# git clone https://github.com/dlfcn-win32/dlfcn-win32.git
# cd dlfcn-win32/
# ./configure
# make
# make install
# cd ..

export CPPFLAGS="-I/usr/include -I/mingw/include ${CPPFLAGS}"
export LDFLAGS="-L/usr/lib -L/mingw/lib ${LDFLAGS}"
export PATH="/usr/bin:${PATH}"
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
make -C back-ends
make -C libhfst
cd ..
