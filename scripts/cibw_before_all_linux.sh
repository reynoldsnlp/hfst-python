#!/bin/bash

# This script is run by cibuildwheel in .github/actions/build.yml
# (specified under CIBW_BEFORE_ALL_LINUX)

set -e -x

# yum update -d 1
yum install -y bison flex libicu-devel readline-devel

# manually install swig 4 since yum has 3 :(
yum install -y pcre-devel
curl https://managedway.dl.sourceforge.net/project/swig/swig/swig-4.0.2/swig-4.0.2.tar.gz > /tmp/swig-4.0.2.tar.gz
pushd /tmp
tar -zxf swig-4.0.2.tar.gz
cd swig-4.0.2
./configure
make
make install
popd


# pypy 2010 manylinux image has outdated bison
BISON_VERSION=$(bison --version | python -c "import re, sys; print(re.search(r'([0-9]+)\.[0-9]+\.[0-9]+.*', sys.stdin.read(), re.S).group(1))")
echo ${BISON_VERSION}
if [[ ${BISON_VERSION} < 3 ]]; then
    echo "Bison is too old. Upgrading...";
    curl http://mirrors.ibiblio.org/gnu/ftp/gnu/bison/bison-3.7.5.tar.gz > /tmp/bison-3.7.5.tar.gz
    pushd /tmp
    tar -zxf bison-3.7.5.tar.gz
    cd bison-3.7.5
    ./configure
    make
    make install
    popd
else
    echo "Bison is new enough. No upgrade needed.";
fi

cd hfst_src/
autoreconf -fvi
./configure --with-readline --with-unicode-handler=icu
make
make check V=1 VERBOSE=1
make install
cd ..

python3 setup.py build_ext
