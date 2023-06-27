set -e -x

brew install icu4c
brew install --force --bottle-tag=arm64_big_sur icu4c

ln -s /usr/local/Cellar/icu4c/73.2/bin/icu-config /usr/local/bin/icu-config
ln -s /usr/local/Cellar/icu4c/73.2/include/* /usr/local/include

curl https://apertium.projectjj.com/osx/nightly/x86_64/hfst-latest.x86_64.tar.bz2 -o hfst-latest.x86_64.tar.bz2
curl https://apertium.projectjj.com/osx/nightly/x86_64/foma-latest.x86_64.tar.bz2 -o foma-latest.x86_64.tar.bz2
mkdir hfst-x86_64
tar -xf hfst-latest.x86_64.tar.bz2 -C hfst-x86_64
tar -xf foma-latest.x86_64.tar.bz2 -C hfst-x86_64
file hfst-x86_64/hfst/lib/* hfst-x86_64/foma/lib/*
# cp -RP hfst-x86_64/hfst/lib/*.dylib /usr/local/lib/
# cp -RP hfst-x86_64/foma/lib/*.dylib /usr/local/lib/

# curl https://apertium.projectjj.com/osx/nightly/arm64/hfst-latest.arm64.tar.bz2  -o hfst-latest.arm64.tar.bz2
# mkdir hfst-arm64
# tar -xf hfst-latest.arm64.tar.bz2 -C hfst-arm64
