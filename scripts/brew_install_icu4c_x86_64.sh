#!/bin/bash

set -e -x

rm -f /usr/local/bin/icu-config
find /usr/local/include/ -lname '/usr/local/Cellar/icu4c/73.2/include/*' -delete
find /usr/local/lib/ -lname '*hfst-arm64/foma/lib/*.dylib' -delete
find /usr/local/lib/ -lname '*hfst-arm64/hfst/lib/*.dylib' -delete
find /usr/local/lib/ -lname '*hfst-x86_64/foma/lib/*.dylib' -delete
find /usr/local/lib/ -lname '*hfst-x86_64/hfst/lib/*.dylib' -delete

brew reinstall icu4c

ln -sF /usr/local/Cellar/icu4c/73.2/bin/icu-config /usr/local/bin/icu-config
ln -sF /usr/local/Cellar/icu4c/73.2/include/* /usr/local/include
ln -sF hfst-x86_64/foma/lib/*.dylib /usr/local/lib/
ln -sF hfst-x86_64/hfst/lib/*.dylib /usr/local/lib/
