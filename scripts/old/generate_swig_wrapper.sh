#!/bin/bash

pushd libhfst_src
git pull origin master
popd

if cmp --silent -- libhfst_src/python/libhfst.i src/hfst/libhfst.i; then
  echo "libhfst.i matches hfst/hfst version."
else
  echo "WARNING: libhfst.i does not match hfst/hfst version."
fi

if cmp --silent -- libhfst_src/python/docstrings.i src/hfst/docstrings.i; then
  echo "docstrings.i matches hfst/hfst version."
else
  echo "WARNING: docstrings.i does not match hfst/hfst version."
fi

swig -c++ -cppext cpp -python -Wall src/hfst/libhfst.i
