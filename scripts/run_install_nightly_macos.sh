#!/bin/bash

if [[ $EUID > 0 ]]; then  
  echo "This script must be run as root/sudo"
  exit 1
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
