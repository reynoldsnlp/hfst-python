#!/bin/bash

# The links in the dylib files do not match the actual filenames.
# This script automatically renames the links using `install_name_tool`.

set -x


wheel_dir=$1
wheel_fname=$2

pushd ${wheel_dir}

unzip -d tmp/ ${wheel_fname}
cd tmp/hfst/.dylibs/
for each_dylib in libhfst*.dylib libicu*.dylib; do
    for link in $(otool -L ${each_dylib} | tail -n +2 | grep libicu | sed "s/(.*)//g" | sed "s/\s+//g"); do
        # get the actual filename
        link_fname=$(ls "$(echo ${link} | rev | cut -d "/" -f 1 | rev | cut -d "." -f 1)"*)
        new_link=$(echo ${link} | sed "s#libicu.*\.dylib#${link_fname}#g")
	sudo install_name_tool -change ${link} ${new_link} ${each_dylib}
    done
done

cd ../..
# zip new wheel
zip -r ${wheel_fname} *

# overwrite the original wheel
mv ${wheel_fname} ${wheel_dir}

# go back to where we started
popd
