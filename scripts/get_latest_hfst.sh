set -e -x

brew install \
    icu4c
#     autoconf \
#     automake \
#     cmake \
#     gawk \
#     gcc \
#     gperftools \
#     help2man \
#     pcre \
#     perl518 \
#     pkg-config \
#     wget

ln -s /usr/local/Cellar/icu4c/73.2/bin/icu-config /usr/local/bin/icu-config
ln -s /usr/local/Cellar/icu4c/73.2/include/* /usr/local/include
# export CPPFLAGS="-I/usr/local/include -I/usr/local//Cellar/icu4c/73.2/include" # -I/usr/local/include/unicode -I/usr/local/opt/icu4c/include"
# export LDFLAGS="-L/usr/local/lib"  # -L/usr/local/opt/bison/lib -L/usr/local/opt/flex/lib -L/usr/local/opt/icu4c/lib"
# export PKG_CONFIG_PATH="/usr/local/opt/icu4c/lib/pkgconfig"

curl https://apertium.projectjj.com/osx/nightly/x86_64/hfst-latest.x86_64.tar.bz2 -o hfst-latest.x86_64.tar.bz2
mkdir hfst-x86_64
tar -xf hfst-latest.x86_64.tar.bz2 -C hfst-x86_64
cp -RP hfst-x86_64/hfst/lib/*.dylib /usr/local/lib/

# curl https://apertium.projectjj.com/osx/nightly/arm64/hfst-latest.arm64.tar.bz2  -o hfst-latest.arm64.tar.bz2
# mkdir hfst-arm64
# tar -xf hfst-latest.arm64.tar.bz2 -C hfst-arm64
