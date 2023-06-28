"""
setup for HFST-swig
"""

from glob import glob
import os
from pathlib import Path
import sys
import sysconfig
import subprocess

from setuptools import Extension
from setuptools import setup


libhfst_src_path = 'libhfst_src/libhfst/src/'
absolute_libhfst_src_path = os.path.abspath(libhfst_src_path)
include_dirs = [absolute_libhfst_src_path]
library_dirs = [absolute_libhfst_src_path + "/.libs"]

extra_link_arguments = []
if sys.platform == "darwin":
    extra_link_arguments.extend(['-mmacosx-version-min=10.7'])
    if os.environ['GITHUB_ACTIONS'] == 'true':
        sysconfig_platform = sysconfig.get_platform()
        local_dir = Path(__file__).parent.absolute()
        print('local_dir: ', local_dir)
        print('sysconfig.get_platform():', sysconfig_platform)
        library_dirs = ['/usr/local/lib']
        include_dirs = [local_dir / 'icu/icu4c/source/common',
                        local_dir / 'hfst-x86_64/hfst/include/hfst']
        print('GLOB', glob('*'))
        print('GLOB', glob('icu/*'))
        print('GLOB', glob(local_dir / 'icu/icu4c/source/common/unicode/unistr.h'))
        print('GLOB', glob(local_dir / 'icu/icu4c/source/common/unicode/uchar.h'))
        if 'x86_64' in sys.executable:
            subprocess.check_call(['./scripts/macos_switch_arch.sh', 'x86_64'])
        elif 'arm64' in sys.executable:
            subprocess.check_call(['./scripts/macos_switch_arch.sh', 'arm64'])
        else:
            raise ValueError("Cannot determine cibuildwheel's target "
                             f"architecture from {sys.executable}.")
if '--local-hfst' in sys.argv:  # If you wish to link to the local HFST library:
    extra_link_arguments.extend(["-Wl,-rpath=" + absolute_libhfst_src_path + "/.libs"])

extra_compile_arguments = ['-std=c++0x']
if sys.platform == "darwin":
    extra_compile_arguments.extend(["-stdlib=libc++", "-mmacosx-version-min=10.7"])

libhfst_module = Extension('hfst._libhfst',
                           language = "c++",
                           sources = ["src/hfst/libhfst.i"],
                           swig_opts = ["-c++",
                                        "-I" + absolute_libhfst_src_path, "-Wall"],
                           include_dirs = include_dirs,
                           library_dirs = library_dirs,
                           libraries = ["hfst"],
                           extra_compile_args = extra_compile_arguments,
                           extra_link_args = extra_link_arguments
                           )

setup(  # see setup.cfg for other configs
      ext_modules = [libhfst_module],
      )
