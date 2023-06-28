#!/bin/bash

set -e -x

for each_arch in arm64 x86_64; do
    curl https://apertium.projectjj.com/osx/nightly/${each_arch}/hfst-latest.${each_arch}.tar.bz2 -o hfst-latest.${each_arch}.tar.bz2
    curl https://apertium.projectjj.com/osx/nightly/${each_arch}/foma-latest.${each_arch}.tar.bz2 -o foma-latest.${each_arch}.tar.bz2
    mkdir hfst-${each_arch}
    tar -xf hfst-latest.${each_arch}.tar.bz2 -C hfst-${each_arch}
    tar -xf foma-latest.${each_arch}.tar.bz2 -C hfst-${each_arch}
    cp -r hfst-${each_arch}/foma/lib/*.dylib hfst-${each_arch}/hfst/lib/
    # cp hfst-${each_arch}/hfst/lib/libhfst.la /usr/local/lib/
    # cp hfst-${each_arch}/hfst/lib/pkgconfig/hfst.pc /usr/local/lib/pkgconfig/
done
