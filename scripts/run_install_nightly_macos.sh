#!/bin/bash

if [[ $EUID > 0 ]]; then  
  echo "This script must be run with root permissions"
fi

if [ -x "$(command -v brew)" ]; then
  brew install \
    autoconf \
    automake \
    cmake \
    gawk \
    gcc \
    gperftools \
    help2man \
    icu4c \
    pcre \
    perl518 \
    pkg-config \
    wget
    # older macos should use apple-gcc42 instead of gcc

    ln -s /usr/local/Cellar/icu4c/<VERSION>/bin/icu-config /usr/local/bin/icu-config
    ln -s /usr/local/Cellar/icu4c/<VERSION>/include/* /usr/local/include
    # export PATH="/usr/local/opt/bison/bin:/usr/local/opt/flex/bin:/usr/local/opt/icu4c/bin:$PATH"
    export CPPFLAGS="-I/usr/local/include -I/usr/local//Cellar/icu4c/73.2/include" # -I/usr/local/include/unicode -I/usr/local/opt/icu4c/include"
    export LDFLAGS="-L/usr/local/lib"  # -L/usr/local/opt/bison/lib -L/usr/local/opt/flex/lib -L/usr/local/opt/icu4c/lib"
    # export PKG_CONFIG_PATH="/usr/local/opt/icu4c/lib/pkgconfig"
elif [ -x "$(command -v port)" ]; then
  sudo port -N install \
    autoconf \
    automake \
    boost \
    cmake \
    expat \
    flex \
    gawk \
    gettext \
    gperf \
    gperftools \
    help2man \
    icu \
    libiconv \
    libtool \
    libxml2 \
    libxslt \
    m4 \
    ncurses \
    p5-locale-gettext \
    pcre \
    perl5 \
    pkgconfig \
    zlib
else
  echo "Neither brew nor Macports available. Aborting..."
  exit 1
fi

curl https://apertium.projectjj.com/osx/install-nightly.sh | bash
