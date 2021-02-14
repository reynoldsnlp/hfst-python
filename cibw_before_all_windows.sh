#!/bin/bash

# set -e -x

# choco install -y --no-progress winflexbison3 swig  # libicu-devel readline-devel
pacman -S --noconfirm --needed  \
          base-devel  \
          bison  \
          flex  \
          mingw-w64-x86_64-toolchain  \
          # mingw-w64-cross-toolchain  \
          mingw-w64-x86_64-libtool  \
          mingw-w64-x86_64-icu  \
          mingw-w64-x86_64-readline  \
          swig

./build_hfst.sh
python setup.py build_ext
