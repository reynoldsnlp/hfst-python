#!/bin/bash

set -e -x
REQ_ARCH=$1

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
    find /usr/local/lib/ -lname "*hfst-${CURR_ARCH}/foma/lib/*.dylib" -delete
    find /usr/local/lib/ -lname "*hfst-${CURR_ARCH}/hfst/lib/*.dylib" -delete

    ln -sF $(pwd)/hfst-${REQ_ARCH}/foma/lib/*.dylib /usr/local/lib/
    ln -sF $(pwd)/hfst-${REQ_ARCH}/hfst/lib/*.dylib /usr/local/lib/
else
    echo "Requested architecture is already installed."
fi
