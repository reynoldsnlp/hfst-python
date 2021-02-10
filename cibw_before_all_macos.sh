#!/bin/bash

set -e -x

brew install swig

pwd
ls
curl https://apertium.projectjj.com/osx/install-release.sh | bash
# cp /usr/local/lib/libhfst.dylib lib/
# ls -l lib/
