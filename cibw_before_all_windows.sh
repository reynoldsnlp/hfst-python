#!/bin/bash

set -e -x

choco install -y --no-progress winflexbison3 swig  # libicu-devel readline-devel

./build_hfst.sh
