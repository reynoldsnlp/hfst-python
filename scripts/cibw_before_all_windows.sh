#!/bin/bash

# This script is run by cibuildwheel in .github/actions/build.yml
# (specified under CIBW_BEFORE_ALL_WINDOWS)


set -e -x

choco upgrade -y --no-progress winflexbison3 swig  # libicu-devel readline-devel
# pacman -S --noconfirm --needed  \
#           base-devel  \
#           bison  \
#           flex  \
#           mingw-w64-x86_64-toolchain  \
#           # mingw-w64-cross-toolchain  \
#           mingw-w64-x86_64-libtool  \
#           mingw-w64-x86_64-icu  \
#           mingw-w64-x86_64-readline  \
#           swig

./scripts/build_hfst.sh
python setup.py build_ext
