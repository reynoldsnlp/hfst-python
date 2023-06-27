#!/bin/bash

set -e -x

curl https://apertium.projectjj.com/osx/nightly/x86_64/hfst-latest.x86_64.tar.bz2 -o hfst-latest.x86_64.tar.bz2
curl https://apertium.projectjj.com/osx/nightly/x86_64/foma-latest.x86_64.tar.bz2 -o foma-latest.x86_64.tar.bz2
mkdir hfst-x86_64
tar -xf hfst-latest.x86_64.tar.bz2 -C hfst-x86_64
tar -xf foma-latest.x86_64.tar.bz2 -C hfst-x86_64
file hfst-x86_64/hfst/lib/* hfst-x86_64/foma/lib/*

curl https://apertium.projectjj.com/osx/nightly/arm64/hfst-latest.arm64.tar.bz2  -o hfst-latest.arm64.tar.bz2
curl https://apertium.projectjj.com/osx/nightly/arm64/foma-latest.arm64.tar.bz2  -o foma-latest.arm64.tar.bz2
mkdir hfst-arm64
tar -xf hfst-latest.arm64.tar.bz2 -C hfst-arm64
tar -xf foma-latest.arm64.tar.bz2 -C hfst-arm64
file hfst-arm64/hfst/lib/* hfst-arm64/foma/lib/*
