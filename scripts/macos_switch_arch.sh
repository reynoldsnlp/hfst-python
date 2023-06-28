#!/bin/bash

set -e -x
REQ_ARCH=$1

ls -l /usr/local/lib/*hfst* || true  # TODO rm
ls -l /usr/local/lib/*foma* || true  # TODO rm

if [[ -e /usr/local/lib/libhfst.dylib ]]; then
    FILE_OUT=$(file /usr/local/lib/libhfst.dylib)
    echo ${FILE_OUT}
    CURR_ARCH=$( echo ${FILE_OUT} | rev | cut -d " " -f 1 | rev)
    echo "Architecture ${CURR_ARCH} is currently installed."
else
    CURR_ARCH=""
    echo "libhfst.dylib is not yet installed in /usr/local/lib/."
fi

if [[ ${CURR_ARCH} != ${REQ_ARCH} ]]; then
    rm -f /usr/local/bin/icu-config
    find /usr/local/include/ -lname '/usr/local/Cellar/icu4c/73.2/include/*' -delete
    find /usr/local/lib/ -lname '*hfst-arm64/foma/lib/*.dylib' -delete
    find /usr/local/lib/ -lname '*hfst-arm64/hfst/lib/*.dylib' -delete
    find /usr/local/lib/ -lname '*hfst-x86_64/foma/lib/*.dylib' -delete
    find /usr/local/lib/ -lname '*hfst-x86_64/hfst/lib/*.dylib' -delete

    # if [[ ${REQ_ARCH} == arm64 ]]; then
    #     brew fetch --force --bottle-tag=arm64_big_sur icu4c
    #     brew install --force $(brew --cache --bottle-tag=arm64_big_sur icu4c)
    # elif [[ ${REQ_ARCH} == x86_64 ]]; then
    #     brew reinstall icu4c
    # fi

    # ln -sF /usr/local/Cellar/icu4c/73.2/bin/icu-config /usr/local/bin/icu-config
    # ln -sF /usr/local/Cellar/icu4c/73.2/include/* /usr/local/include
    ln -sF $(pwd)/hfst-${REQ_ARCH}/foma/lib/*.dylib /usr/local/lib/
    ln -sF $(pwd)/hfst-${REQ_ARCH}/hfst/lib/*.dylib /usr/local/lib/
else
    echo "Requested architecture is already installed."
fi
