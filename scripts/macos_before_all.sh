#!/bin/bash

set -e -x

git submodule init
git submodule update

for each_arch in arm64 x86_64; do
    curl https://apertium.projectjj.com/osx/nightly/${each_arch}/hfst-latest.${each_arch}.tar.bz2 -o hfst-latest.${each_arch}.tar.bz2
    curl https://apertium.projectjj.com/osx/nightly/${each_arch}/foma-latest.${each_arch}.tar.bz2 -o foma-latest.${each_arch}.tar.bz2
    mkdir hfst-${each_arch}
    tar -xf hfst-latest.${each_arch}.tar.bz2 -C hfst-${each_arch}
    tar -xf foma-latest.${each_arch}.tar.bz2 -C hfst-${each_arch}
    cp -r hfst-${each_arch}/foma/lib/*.dylib hfst-${each_arch}/hfst/lib/
done

brew uninstall --ignore-dependencies icu4c

ICU_VERSION=$(ls hfst-x86_64/hfst/lib/libicudata.*.*.dylib | sed "s/.dylib$//g" | sed "s/.*libicudata\.//g" | sed "s/\./-/g")
ICU_VERSION_=$(echo ${ICU_VERSION} | sed "s/-/_/g")

curl -L https://github.com/unicode-org/icu/releases/download/release-${ICU_VERSION}/icu4c-${ICU_VERSION_}-src.tgz -o icu.tar.gz
tar -xzf icu.tar.gz
