#!/bin/bash

git submodule update --init --recursive
cd libhfst_src/
git reset --hard
autoreconf -i
./configure --with-unicode-handler=icu  # TODO --with-readline?
make -C back-ends
make -C libhfst
cd ..

swig -c++ -cppext cpp -python -Ilibhfst_src/libhfst/src/ -Wall src/hfst/libhfst.i
