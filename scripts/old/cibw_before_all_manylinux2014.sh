#!/bin/bash

# This script is run by cibuildwheel in .github/actions/build.yml
# (specified under CIBW_BEFORE_ALL_LINUX)

set -e -x

# yum update -d 1
yum install -y bison flex libicu-devel readline-devel

# bash scripts/install_swig_from_src.sh
bash scripts/install_bison_from_src.sh

cd libhfst_src/
autoreconf -fvi
./configure --with-unicode-handler=icu
make -C back-ends
make -C libhfst
cd ..
