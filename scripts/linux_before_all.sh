set -e -x

git submodule init
git submodule update

if [ -x "$(command -v dnf)" ]; then
    PM=dnf
    ${PM} install -y gcc-toolset-12-libatomic-devel
elif [ -x "$(command -v yum)" ]; then
    PM=yum
else
    echo "Neither dnf or yum found. Exiting."
    exit 1
fi

${PM} install -y autoconf automake bison flex libicu-devel libtool pkgconfig readline-devel swig zlib-devel

git clone https://github.com/apertium/packaging.git

# build foma
git clone https://github.com/mhulden/foma.git
pushd foma/foma/
cmake -DCMAKE_INSTALL_LIBDIR=lib .
make && make install
# foma installs to the wrong local folder, so fix that
cp -av /usr/local/lib64/* /usr/local/lib/ || true  # allow this command to fail
ldconfig 
popd

# build openfst
curl https://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.7.9.tar.gz -o openfst-1.7.9.tar.gz
tar -xzf openfst-1.7.9.tar.gz
pushd openfst-1.7.9/
patch -p1 <../packaging/tools/openfst/debian/patches/openfst-atomic.diff
HFST_ARCH=$(uname -m)
echo ${HFST_ARCH}
if [[ ${HFST_ARCH} == 'arm64' ]]; then
  patch -p1 <../packaging/tools/openfst/debian/patches/openfst-sse.diff
fi
grep c++17 configure.ac  # check that patches applied correctly
autoreconf -fvi
./configure --enable-bin --enable-compact-fsts --enable-compress --enable-const-fsts --enable-far --enable-fsts --enable-grm --enable-linear-fsts --enable-lookahead-fsts --enable-mpdt --enable-ngram-fsts --enable-pdt --enable-special --disable-static
make && make install
popd

# build libhfst
pushd libhfst_src/
autoreconf -fvi
./configure --disable-static --with-unicode-handler=icu --with-openfst-upstream --with-foma-upstream
make && make install
popd

# generate SWIG bindings
swig -c++ -cppext cpp -python -Wall src/hfst/libhfst.i
