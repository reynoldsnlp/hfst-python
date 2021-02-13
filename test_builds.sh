#!/bin/bash

# Run tests using all python interpreters given
# Usage: ./test_builds.sh path/to/python1 path/to/python2 ...

cd test
for py in "$@"; do
    FULL_PY=$(${py} -c "import sys; print(sys.executable)")
    echo ${FULL_PY}
    ${FULL_PY} --version
    ${FULL_PY} -m pip install --user --no-index -f ../wheelhouse/ --force-reinstall hfst
    ${FULL_PY} -c "import hfst"
    ./test.sh --python "${FULL_PY}"
    ${FULL_PY} -m pip uninstall -y hfst
done
cd ..
