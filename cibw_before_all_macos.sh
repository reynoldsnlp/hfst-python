#!/bin/bash

set -e -x

brew install autoconf automake python3-setuptools swig bison flex libicu-dev  \
	libreadline-dev libtool

source ./build_hfst.sh
