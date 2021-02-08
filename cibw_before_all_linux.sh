#!/bin/bash

set -e -x

apt-get -qy update
apt-get -qfy install --no-install-recommends build-essential automake  \
	autotools-dev pkg-config python3-dev python3-setuptools swig bison  \
	flex libicu-dev libreadline-dev libtool zlib1g-dev

./build_hfst.sh
