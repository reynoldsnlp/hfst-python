set -e -x

uname -m
python -c "import platform; print('version:', platform.version()); print('uname:', platform.uname())"

# Set environment variables
