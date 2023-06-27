#!/bin/bash

set -e -x

rm -f /usr/local/bin/icu-config
find /usr/local/include/ -lname '/usr/local/Cellar/icu4c/73.2/include/*' -delete
find /usr/local/lib/ -lname '*hfst-arm64/foma/lib/*.dylib' -delete
find /usr/local/lib/ -lname '*hfst-arm64/hfst/lib/*.dylib' -delete
find /usr/local/lib/ -lname '*hfst-x86_64/foma/lib/*.dylib' -delete
find /usr/local/lib/ -lname '*hfst-x86_64/hfst/lib/*.dylib' -delete

brew fetch --force --bottle-tag=arm64_big_sur icu4c
brew install --force $(brew --cache --bottle-tag=arm64_big_sur icu4c)

ln -sF /usr/local/Cellar/icu4c/73.2/bin/icu-config /usr/local/bin/icu-config
ln -sF /usr/local/Cellar/icu4c/73.2/include/* /usr/local/include
ln -sF hfst-arm64/foma/lib/*.dylib hfst-arm64/foma/lib/*.la /usr/local/lib/
ln -sF hfst-arm64/hfst/lib/*.dylib hfst-arm64/hfst/lib/*.la /usr/local/lib/

ls -l /usr/local/lib
