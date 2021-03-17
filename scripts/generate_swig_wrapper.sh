#!/bin/bash

git submodule update --init --recursive
cd libhfst_src/
git reset --hard
autoreconf -i
./configure --with-unicode-handler=icu  # TODO --with-readline?

cd back-ends
make
cd ../

cd libhfst/
make
cd ../../

swig -c++ -cppext cpp -python -Ilibhfst_src/libhfst/src/ -Wall src/hfst/libhfst.i
