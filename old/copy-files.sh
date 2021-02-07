#!/bin/sh

##### This file may not be needed anymore, since the hfst source is now
##### a submodule.

## Copy files needed for a pypi distribution for linux or os x.
## copy-files-win.sh is the equivalent script for windows environment.

set -x

if [ "$1" = "--help" -o "$1" = "-h" ]; then
    echo "copy-files.sh [--with-c-foma]"
    echo ""
    echo "Copy files needed for a pypi distribution on linux and OS X."
    echo ""
    echo "--with-c-foma:   copy the C version of foma backend (instead of C++)"
    echo ""
    echo "NOTE: flex/bison-generated cc and hh files are copied as such to"
    echo "avoid dependency on swig. Make sure you have a fresh version of them"
    echo "(run 'make' in top directory, if needed)."
    echo ""
    exit 0
fi

CPP_FOMA="true"
if [ "$1" = "--with-c-foma" ]; then
    CPP_FOMA="false"
fi

if ! [ -d "back-ends" ]; then mkdir back-ends; fi
if ! [ -d "libhfst" ]; then mkdir libhfst; fi
if ! [ -d "hfst" ]; then mkdir hfst; fi


for file in libhfst.i libhfst.py docstrings.i ;
do
    cp ../$file $file
done

# Copy all files that have a c++ version as backend files to be compiled.
if [ "$CPP_FOMA" = "true" ]; then
    cp back-ends/foma/cpp-version/* back-ends/foma/
fi

# .cc -> .cpp
for dir in back-ends libhfst;
do
    find $dir -name "*.cc" | sed 's/\(.*\).cc/mv \1.cc \1.cpp/' | sh
done
