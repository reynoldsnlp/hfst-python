#!/bin/bash

BISON_VERSION=$(bison --version | python -c "import re, sys; print(re.search(r'([0-9]+)\.([0-9]+)\.([0-9]+)', sys.stdin.read(), re.S).groups())")
echo "Current bison version: ${BISON_VERSION}"
if [[ $( echo ${BISON_VERSION} | python -c "import sys; v = eval(sys.stdin.read().replace('\'', '')); print(v >= (3, 0, 0))" ) == *"False"* ]]; then
    echo "Bison is too old. Upgrading...";
    yum remove -y bison
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

FLEX_VERSION=$(flex --version | python -c "import re, sys; print(re.search(r'([0-9]+)\.([0-9]+)\.([0-9]+)', sys.stdin.read(), re.S).groups())")
echo "Current flex version: ${FLEX_VERSION}"
if [[ $( echo ${FLEX_VERSION} | python -c "import sys; v = eval(sys.stdin.read().replace('\'', '')); print(v >= (2, 6, 0))" ) == *"False"* ]]; then
    echo "Flex is too old. Upgrading...";
    yum remove -y flex
    pushd /tmp
    wget https://github.com/westes/flex/files/981163/flex-2.6.4.tar.gz
    tar -zxf flex-2.6.4.tar.gz
    cd flex-2.6.4
    ./configure
    make
    make install
    popd
else
    echo "Flex is new enough. No upgrade needed.";
fi
