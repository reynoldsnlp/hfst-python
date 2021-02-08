#!/bin/bash

set -e -x

PYTHON_EXECUTABLES="python3.6 python3.7 python3.8 python3.9"

for p in ${PYTHON_EXECUTABLES}; do
    ${p} -m pip install --user --upgrade setuptools twine wheel
done

echo "STEP Cleaning old files..."
./clean.sh

echo "STEP Building HFST C++..."
cd hfst_src/
autoreconf -i  # Is this necessary?
./configure --enable-all-tools --with-readline --enable-fsmbook-tests
# make clean
make  # TODO only libhfst/src/parsers/ and a few other things?
cd ..

echo "STEP Copying dylib..."
cp hfst_src/libhfst/src/.libs/libhfst.dylib hfst/lib/

echo "STEP Building binary distribution wheels..."
for p in ${PYTHON_EXECUTABLES}; do
    ${p} setup.py build_ext  --with-libc++ --local-hfst --inplace  \
            | tee build_ext_output.tmp
    SO_FILE=$(grep "^copying build/lib\..*/_libhfst\..*\.so" build_ext_output.tmp  \
              | cut -d " " -f 2)
    OLD_DYLIB=$(otool -L ${SO_FILE}  \
                | egrep "^\s+.*libhfst"  \
		| sed -r "s/^\t(.*dylib).*/\1/g")
    install_name_tool -change ${OLD_DYLIB} "@loader_path/lib/libhfst.dylib" ${SO_FILE}
    install_name_tool -change ${OLD_DYLIB} "@loader_path/lib/libhfst.dylib" "hfst/$(basename ${SO_FILE})"
    rm build_ext_output.tmp
    ${p} setup.py bdist_wheel --with-libc++
done

echo "STEP Building source distribution..."
${p} setup.py sdist --with-libc++

echo "STEP Running tests..."
./test_builds.sh ${PYTHON_EXECUTABLES}
