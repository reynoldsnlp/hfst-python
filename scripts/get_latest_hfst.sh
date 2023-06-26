set -e -x

curl https://apertium.projectjj.com/osx/nightly/x86_64/hfst-latest.x86_64.tar.bz2 -o hfst-latest.x86_64.tar.bz2
curl https://apertium.projectjj.com/osx/nightly/arm64/hfst-latest.arm64.tar.bz2  -o hfst-latest.arm64.tar.bz2
tar -xf hfst-latest.x86_64.tar.bz2 -C hfst-x86_64
tar -xf hfst-latest.arm64.tar.bz2 -C hfst-arm64

uname -m
python -c "import platform; print('version:', platform.version()); print('uname:', platform.uname())"

. scripts/run_install_nightly_macos.sh

# Set environment variables
