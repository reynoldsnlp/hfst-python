set -e  # stop script on error
set -x  # print commands as they are executed

dnf install -y flex bison readline-devel libicu-devel libtool swig pkgconfig readline-devel zlib-devel autoconf automake gcc-toolset-12-libatomic-devel

# get foma
git clone https://github.com/mhulden/foma.git
pushd foma/foma/
cmake .
make && make install
# foma installs to the wrong local folder, so fix that
cp -av /usr/local/lib64/* /usr/local/lib/
ldconfig 
popd

curl https://www.openfst.org/twiki/pub/FST/FstDownload/openfst-1.7.9.tar.gz -o openfst-1.7.9.tar.gz
tar -xzf openfst-1.7.9.tar.gz
pushd openfst-1.7.9/
autoreconf -fvi
./configure
make && make install
popd

git clone https://github.com/hfst/hfst.git libhfst
pushd libhfst/
autoreconf -fvi
# ./configure --disable-static --with-unicode-handler=icu --with-openfst-upstream --with-foma-upstream
./configure --disable-static --enable-all-tools --with-readline --with-unicode-handler=icu --with-openfst-upstream --with-foma-upstream
make && make install
popd

# swig -c++ -cppext cpp -python -Wall src/hfst/libhfst.i
