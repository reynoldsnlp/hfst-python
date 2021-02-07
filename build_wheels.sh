#!/bin/bash

set -e -x

export LDFLAGS="-Wl,-headerpad_max_install_names"

PYTHON_EXECUTABLES="python3.9"
# PYTHON_EXECUTABLES="python3.6 python3.7 python3.8 python3.9"

for p in ${PYTHON_EXECUTABLES}; do
    ${p} -m pip install --user --upgrade setuptools twine wheel
    # ${p} -m pip uninstall hfst
done

echo "STEP Cleaning old files..."
./clean.sh

echo "STEP Building HFST..."
./build_hfst.sh

echo "STEP Building binary distribution wheels..."
case "$(uname -s)" in
    Darwin)  # macOS / OS X
        echo "macOS build"
        cp hfst_src/libhfst/src/.libs/libhfst.*.dylib hfst/lib/
        for p in ${PYTHON_EXECUTABLES}; do
            ${p} -m pip install --user --upgrade delocate
            ${p} setup.py build_ext  --with-libc++ --local-hfst --inplace  \
                | ${p} get_so_name.py  \
                > so_filenames.tmp
            DYLIB=$(basename hfst/lib/libhfst*.dylib)
            for so_file in $(cat so_filenames.tmp); do
                install_name_tool -change "/usr/local/lib/${DYLIB}" "@loader_path/lib/${DYLIB}" ${so_file}
                install_name_tool -change "/usr/local/lib/${DYLIB}" "@loader_path/lib/${DYLIB}" "hfst/$(basename ${so_file})"
            done
            rm so_filenames.tmp
            ${p} setup.py bdist_wheel --with-libc++  --local-hfst
        done

        ;;

    Linux)
        echo 'Linux build'
        ;;

    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        echo 'TODO Add script here for Windows build'
        ;;

    *)
        echo 'This operating system is not supported'
        ;;
esac

echo "STEP Building source distribution..."
${p} setup.py sdist --with-libc++ --local-hfst


echo "STEP Running tests..."
./test_builds.sh ${PYTHON_EXECUTABLES}
