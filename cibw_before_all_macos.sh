#!/bin/bash

set -e -x

brew install swig

curl https://apertium.projectjj.com/osx/install-release.sh | bash
pwd
ls
cp /usr/local/lib/libhfst.dylib lib/
ls -l lib/
