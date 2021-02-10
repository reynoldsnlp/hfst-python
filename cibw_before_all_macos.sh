#!/bin/bash

set -e -x

brew install swig

pwd
ls
curl https://apertium.projectjj.com/osx/nightly/hfst-latest.tar.bz2 > tmp/hfst-latest.tar.bz2
cd tmp
tar -xzf hfst-latest.tar.bz2
cd ..

cp tmp/hfst/lib/libhfst.dylib lib/
