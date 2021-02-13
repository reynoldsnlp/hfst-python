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

./build_hfst.sh
python setup.py build_ext
