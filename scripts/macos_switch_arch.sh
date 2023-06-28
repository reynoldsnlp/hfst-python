#!/bin/bash

set -e -x
REQ_ARCH=$1

ls -l /usr/local/lib/*hfst*  # TODO rm
ls -l /usr/local/lib/*foma*  # TODO rm

CURR_ARCH=$(file /usr/local/lib/libhfst.dylib | rev | cut -d " " -f 1 | rev)
echo "Architecture ${CURR_ARCH} is currently installed."

if [[ ${CURR_ARCH} != ${REQ_ARCH} ]]; then
    rm -f /usr/local/bin/icu-config
    find /usr/local/include/ -lname '/usr/local/Cellar/icu4c/73.2/include/*' -delete
    find /usr/local/lib/ -lname '*hfst-arm64/foma/lib/*.dylib' -delete
    find /usr/local/lib/ -lname '*hfst-arm64/hfst/lib/*.dylib' -delete
    find /usr/local/lib/ -lname '*hfst-x86_64/foma/lib/*.dylib' -delete
    find /usr/local/lib/ -lname '*hfst-x86_64/hfst/lib/*.dylib' -delete

    if [[ ${REQ_ARCH} == arm64 ]]; then
        brew fetch --force --bottle-tag=arm64_big_sur icu4c
        brew install --force $(brew --cache --bottle-tag=arm64_big_sur icu4c)
    elif [[ ${REQ_ARCH} == x86_64 ]]; then
        brew reinstall icu4c
    fi

    ln -sF /usr/local/Cellar/icu4c/73.2/bin/icu-config /usr/local/bin/icu-config
    ln -sF /usr/local/Cellar/icu4c/73.2/include/* /usr/local/include
    ln -sF $(pwd)/hfst-arm64/foma/lib/*.dylib /usr/local/lib/
    ln -sF $(pwd)/hfst-arm64/hfst/lib/*.dylib /usr/local/lib/
fi
