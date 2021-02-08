#!/bin/bash

set -e -x

brew install automake glib swig
uconv -V

source ./build_hfst.sh
