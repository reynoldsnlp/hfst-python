#!/bin/bash

set -e -x

yum install -y flex libicu-devel readline-devel

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

./build_hfst.sh
python setup.py build_ext
