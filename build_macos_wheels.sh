#!/bin/bash

set -e -x

PYTHON_EXECUTABLES="python3.6"
# PYTHON_EXECUTABLES="python3.6 python3.7 python3.8 python3.9"

# for p in ${PYTHON_EXECUTABLES}; do
# 	${p} -m pip install --user --upgrade setuptools twine wheel
# 	# ${p} -m pip uninstall hfst
# done

echo "STEP Cleaning old files..."
./clean.sh

echo "STEP Configuring..."
# cd hfst_src/
# autoreconf -i  # Is this necessary?
# ./configure --enable-all-tools --with-readline --enable-fsmbook-tests
# # make clean
# make

# echo "STEP Making flex/yacc files..."
# cd libhfst/src/parsers/
# make  # this is unnecessary if `make` is already called in the root dir, but it doesn't hurt
# cd ../../../../

echo "STEP Copying cpp and other files..."
# ./copy-files.sh
# TODO renaming *.cc to *.cpp might be necessary on Windows.

echo "STEP Building binary distribution wheels..."
for p in ${PYTHON_EXECUTABLES}; do
	${p} setup.py build_ext  --with-libc++ --local-hfst --inplace  \
                | ${p} get_so_name.py  \
                > so_filenames.tmp
            DYLIB=$(basename hfst/lib/libhfst*.dylib)
            for so_file in $(cat so_filenames.tmp); do
                install_name_tool -change "/usr/local/lib/${DYLIB}" "@loader_path/lib/libhfst.dylib" ${so_file}
                install_name_tool -change "/usr/local/lib/${DYLIB}" "@loader_path/lib/libhfst.dylib" "hfst/$(basename ${so_file})"
            done
            rm so_filenames.tmp
	${p} setup.py bdist_wheel --with-libc++
done

echo "STEP Building source distribution..."
${p} setup.py sdist --with-libc++

echo "STEP Running tests..."
./test_builds.sh ${PYTHON_EXECUTABLES}
