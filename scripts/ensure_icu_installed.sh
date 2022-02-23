#!/bin/bash

set -e -x

# 2010 manylinux image has outdated icu
ICU_VERSION=$(icu-config --version | cut -d . -f 1)
echo "ICU version: ${ICU_VERSION}"
if [[ ${ICU_VERSION} < 50 ]]; then
    echo "ICU is too old. Upgrading...";
    pushd /tmp
    curl -L https://github.com/unicode-org/icu/releases/download/release-70-1/icu4c-70_1-src.tgz > icu4c-70_1-src.tgz
    tar -zxf icu4c-70_1-src.tgz
    cd icu/source
    chmod +x runConfigureICU configure install-sh

    yum install -y rh-python35.x86_64
    mv /usr/bin/python /usr/bin/python_old
    ln -s /usr/local/bin/python3.9 /usr/bin/python
    ./runConfigureICU $1
    rm /usr/bin/python
    mv /usr/bin/python_old /usr/bin/python

    gmake
    gmake install
    popd
else
    echo "ICU is new enough. No upgrade needed.";
fi
