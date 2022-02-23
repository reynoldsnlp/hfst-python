#!/bin/bash

# pypy 2010 manylinux image has outdated bison
BISON_VERSION=$(bison --version | python -c "import re, sys; print(re.search(r'([0-9]+)\.[0-9]+\.[0-9]+.*', sys.stdin.read(), re.S).group(1))")
echo ${BISON_VERSION}
if [[ ${BISON_VERSION} < 3 ]]; then
    echo "Bison is too old. Upgrading...";
    curl http://mirrors.syringanetworks.net/gnu/bison/bison-3.8.2.tar.gz > /tmp/bison-3.8.2.tar.gz
    pushd /tmp
    tar -zxf bison-3.8.2.tar.gz
    cd bison-3.8.2
    ./configure
    make
    make install
    popd
else
    echo "Bison is new enough. No upgrade needed.";
fi
