set -e -x

curl https://apertium.projectjj.com/osx/nightly/x86_64/hfst-latest.x86_64.tar.bz2 -o hfst-latest.x86_64.tar.bz2
mkdir hfst-x86_64
tar -xf hfst-latest.x86_64.tar.bz2 -C hfst-x86_64

curl https://apertium.projectjj.com/osx/nightly/arm64/hfst-latest.arm64.tar.bz2  -o hfst-latest.arm64.tar.bz2
mkdir hfst-arm64
tar -xf hfst-latest.arm64.tar.bz2 -C hfst-arm64

# . scripts/run_install_nightly_macos.sh
