#!/bin/bash

# Run tests using all python interpreters given
# Usage: ./test_builds.sh path/to/python1 path/to/python2 ...

cd test
for py in "$@"; do
	${py} -c "import sys; print(sys.executable)"
	${py} -m pip install --user --no-index -f ../dist/ --force-reinstall hfst
	${py} -c "import hfst"
	./test.sh --python "${py}"
	${py} -m pip uninstall -y hfst
done
cd ..
