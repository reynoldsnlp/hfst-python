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
if [[ ${BISON_VERSION} -le 7 ]]; then
    echo "Bison is too old. Upgrading...";
    curl http://springdale.princeton.edu/data/springdale/6/x86_64/os/Computational/bison3-3.0.2-3.sdl6.x86_64.rpm > bison3-3.0.2-3.sdl6.x86_64.rpm
    rpm -Uvh springdale-computational*rpm
    yum install -y bison3
else
    echo "Bison is new enough. No upgrade needed.";
fi

./build_hfst.sh
python setup.py build_ext
