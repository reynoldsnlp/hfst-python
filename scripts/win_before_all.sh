#!/bin/bash

# This script is run by cibuildwheel.
# See either .github/actions/build.yml (CIBW_BEFORE_ALL_WINDOWS)
# or pyproject.toml (before-all-windows)

set -e -x

git submodule init
git submodule update

pacman -S --noconfirm --needed  \
    bison  \
    flex  \
    mingw-w64-clang-i686-autotools  \
    mingw-w64-clang-x86_64-autotools  \
    mingw-w64-clang-aarch64-autotools  \
    mingw-w64-i686-autotools  \
    mingw-w64-x86_64-autotools  \
    mingw-w64-clang-i686-dlfcn  \
    mingw-w64-clang-x86_64-dlfcn  \
    mingw-w64-clang-aarch64-dlfcn  \
    mingw-w64-i686-dlfcn  \
    mingw-w64-x86_64-dlfcn  \
    mingw-w64-clang-i686-icu  \
    mingw-w64-clang-x86_64-icu  \
    mingw-w64-clang-aarch64-icu  \
    mingw-w64-i686-icu  \
    mingw-w64-x86_64-icu  \
    mingw-w64-clang-i686-readline  \
    mingw-w64-clang-x86_64-readline  \
    mingw-w64-clang-aarch64-readline  \
    mingw-w64-i686-readline  \
    mingw-w64-x86_64-readline  \
    mingw-w64-clang-i686-zlib  \
    mingw-w64-clang-x86_64-zlib  \
    mingw-w64-clang-aarch64-zlib  \
    mingw-w64-i686-zlib  \
    mingw-w64-x86_64-zlib  \
    swig

export CPPFLAGS="-I/c/msys64/mingw64/include -I/c/msys64/mingw32/include -I/usr/include -I/mingw/include ${CPPFLAGS}"
export LDFLAGS="-L/c/msys64/var/lib/pacman/local -L/c/msys64/mingw64/lib -L/c/msys64/mingw32/lib -L/usr/lib -L/mingw/lib ${LDFLAGS}"
export PATH="/c/msys64/mingw64/bin:/c/msys64/mingw32/bin:/usr/bin:${PATH}"
export PKG_CONFIG_PATH="/c/msys64/mingw64/lib/pkgconfig:/c/msys64/mingw32/lib/pkgconfig:/usr/lib/pkgconfig:${PKG_CONFIG_PATH}"

git clone https://github.com/apertium/packaging.git

# get foma
git clone https://github.com/mhulden/foma.git
pushd foma/foma/
cmake .
make && make install
popd

curl https://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.7.9.tar.gz -o openfst-1.7.9.tar.gz
tar -xzf openfst-1.7.9.tar.gz
pushd openfst-1.7.9/
patch -p1 <../packaging/tools/openfst/debian/patches/openfst-cxx17.diff
patch -p1 <../packaging/tools/openfst/debian/patches/openfst-sse.diff
grep c++17 configure.ac  # check that patches applied correctly
autoreconf -fvi
./configure --enable-bin --enable-compact-fsts --enable-compress --enable-const-fsts --enable-far --enable-fsts --enable-grm --enable-linear-fsts --enable-lookahead-fsts --
enable-mpdt --enable-ngram-fsts --enable-pdt --enable-special --disable-static
make && make install
popd

pushd libhfst_src/
autoreconf -fvi
./configure --enable-mingw --disable-static --with-unicode-handler=icu --with-foma-upstream --with-openfst-upstream
make && make install
popd

# generate SWIG bindings
swig -c++ -cppext cpp -python -Wall src/hfst/libhfst.i
