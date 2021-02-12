#!/bin/bash

set -e -x

choco install -y bison flex swig  # libicu-devel readline-devel

./build_hfst.sh
