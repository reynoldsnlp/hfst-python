#!/bin/bash

set -e -x

# apt-get -qfy install --no-install-recommends build-essential automake  \
# 	autotools-dev pkg-config python3-dev python3-setuptools swig bison  \
# 	flex libicu-dev libreadline-dev libtool zlib1g-dev

# manually install swig 4 since yum has 3 :(
yum update -d1 && yum install -y bison flex libicu-devel
yum install -y pcre pcre-devel  # needed to compile swig
curl https://managedway.dl.sourceforge.net/project/swig/swig/swig-4.0.2/swig-4.0.2.tar.gz \
        -o /tmp/swig-4.0.2.tar.gz
pushd /tmp
tar -zxf swig-4.0.2.tar.gz
cd swig-4.0.2
./configure
make
make install
popd

./build_hfst.sh
