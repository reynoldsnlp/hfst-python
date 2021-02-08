#!/bin/bash

set -e -x

brew update
brew install build-essential automake autotools-dev pkg-config python3-dev  \
        python3-setuptools swig bison flex libicu-dev libreadline-dev  \
	libtool zlib1g-dev

source ./build_hfst.sh
