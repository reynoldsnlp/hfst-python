#!/usr/bin/python3

"""
Setup for creating PIP packages for HFST Python bindings.

Before running setup, make sure that the following C++ files
from 'libhfst_src/libhfst/src/parsers' have been generated from flex/yacc files
before copying (on linux and OS X by running 'make' and on windows
with 'compile-parsers-win.sh' located in 'libhfst_src/libhfst/src/parsers'):

  lexc-lexer.cc pmatch_lex.cc xfst-lexer.cc xre_lex.cc sfst-scanner.cc
  lexc-parser.cc pmatch_parse.cc xfst-parser.cc xre_parse.cc sfst-compiler.cc
  lexc-parser.hh pmatch_parse.hh xfst-parser.hh xre_parse.hh sfst-compiler.hh

Compiling the extensions requires python, swig and a C++ compiler,
all located on a directory listed on system PATH. On linux and OS X,
readline and getline must be available.

The setup script has been tested on linux with gcc 5.4.0, swig 3.0.12 and
python 3.5 and on windows with swig 3.0.5 and msvc 10.0 (with python 3.4)
and msvc 14.0 (with python 3.5 and 3.6).

"""

from glob import glob
import os
from pprint import pprint
import re
from setuptools import Extension
from setuptools import setup
import sys
from sys import platform
from sys import version_info

# default to 10.9, unless the environment variable is set to something else
MACOSX_VERSION_MIN = os.environ.get('MACOSX_DEPLOYMENT_TARGET', '10.9')

# Whether to use the C++ version of the foma back-end
FOMA_CPP = True

# ----- SWIG CONFIGURATION -----

# HFST C++ headers needed by swig when creating the python/c++ interface
abs_libhfst_src_dir = os.path.abspath('libhfst_src/libhfst/src/')

# Generate wrapper for C++
ext_swig_opts = ['-c++', '-I' + abs_libhfst_src_dir, '-Wall']

# ----- LINKER ARGUMENTS -----

# Readline is needed for hfst.start_xfst(). On windows the shell where HFST
# python bindings are run from has its own readline which will do.
include_readline = False
include_getline = False
if platform.startswith('linux') or platform == 'darwin':
    include_readline = True
    include_getline = True
ext_extra_link_args = []
if include_readline:
    ext_extra_link_args = ['-lreadline']
if platform == 'darwin':
    ext_extra_link_args.extend(['-mmacosx-version-min=' + MACOSX_VERSION_MIN])


# ----- INCLUDE DIRECTORIES -----

# HFST headers needed when compiling the actual c++ extension
ext_include_dirs = [os.path.abspath('./libhfst_src'),  # config.h
                    os.path.abspath('./libhfst_src/back-ends'),
                    # os.path.abspath('./libhfst_src/back-ends/dlfcn'),
                    # os.path.abspath('./libhfst_src/back-ends/sfst'),
                    os.path.abspath('./libhfst_src/libhfst/src'),
                    # os.path.abspath('./libhfst_src/libhfst/src/implementations'),
                    # os.path.abspath('./libhfst_src/libhfst/src/implementations/compose_intersect'),
                    # os.path.abspath('./libhfst_src/libhfst/src/implementations/optimized-lookup'),
                    os.path.abspath('./libhfst_src/libhfst/src/parsers'),
                    # os.path.abspath('./libhfst_src/libhfst/src/parsers/alphabet_src'),
                    # os.path.abspath('./libhfst_src/libhfst/src/parsers/io_src'),
                    # os.path.abspath('./libhfst_src/libhfst/src/parsers/rule_src'),
                    # os.path.abspath('./libhfst_src/libhfst/src/parsers/string_src'),
                    # os.path.abspath('./libhfst_src/libhfst/src/parsers/variable_src')
                    ]
if FOMA_CPP:
    ext_include_dirs.append(os.path.abspath('./libhfst_src/back-ends/foma/cpp-version'))
    # some headers are only in foma/
    ext_include_dirs.append(os.path.abspath('./libhfst_src/back-ends/foma'))
else:
    ext_include_dirs.append(os.path.abspath('./libhfst_src/back-ends/foma'))
if platform == 'win32':
    ext_include_dirs.append(os.path.abspath('./libhfst_src/back-ends/dlfcn'))
    ext_include_dirs.append(os.path.abspath('./libhfst_src/back-ends/openfstwin/src/include'))
    # ext_include_dirs.append(os.path.abspath('./libhfst_src/back-ends/openfstwin/src/include/fst'))
else:
    ext_include_dirs.append(os.path.abspath('./libhfst_src/back-ends/openfst/src/include'))
    # ext_include_dirs.append(os.path.abspath('./libhfst_src/back-ends/openfst/src/include/fst'))


# -----  MACROS CONFIGURATION  -----

ext_define_macros = []
ext_define_macros.append(('HAVE_FOMA', None))
ext_define_macros.append(('HAVE_OPENFST', None))
ext_define_macros.append(('HAVE_OPENFST_LOG', None))

if include_readline:
    ext_define_macros.append(('HAVE_READLINE', None))
if include_getline:
    ext_define_macros.append(('HAVE_GETLINE', None))

# msvc-specific macros.
if platform == 'win32':
    # MSC_VER_ should already be defined
    for macro in ['HFSTEXPORT', 'OPENFSTEXPORT', 'WINDOWS', 'WIN32',
                  '_CRT_SECURE_NO_WARNINGS']:
        ext_define_macros.append((macro, None))

# If C++11 is not supported, what features will be disabled and where unordered
# map and set are found.
# if platform == 'win32':
    # Disable c++11 features.
    # ext_define_macros.append(('NO_CPLUSPLUS_11', None))
    # Unordered containers are in namespace std::tr1.
    # ext_define_macros.append(('USE_TR1_UNORDERED_MAP_AND_SET', None))
    # On windows, the header files are not located in directory tr1
    # although the namespace is std::tr1.
#     if platform != 'win32':
#         ext_define_macros.append(('INCLUDE_TR1_UNORDERED_MAP_AND_SET', None))


# ----- COMPILATION OPTIONS -----

ext_extra_compile_args = []
if platform.startswith('linux'):
    ext_extra_compile_args = ['-Wno-sign-compare', '-std=c++11']
elif platform == 'darwin':
    ext_extra_compile_args.extend(['-std=c++11', '-stdlib=libc++',
                                   '-mmacosx-version-min=' + MACOSX_VERSION_MIN,
                                   '-Wno-sign-compare'])
elif platform == 'win32':
    # define error handling mechanism on windows
    ext_extra_compile_args = ['/EHsc']


# ----- C++ SOURCE FILES -----


def glob_cpp(dir):
    """Glob of c/cc/cpp files."""
    fnames = []
    for pattern in ['*.c', '*.cc', '*.cpp']:
        fnames += glob(os.path.join(dir, pattern))
    return fnames


if FOMA_CPP:
    foma_glob_pattern = 'libhfst_src/back-ends/foma/cpp-version/*.cc'
else:
    foma_glob_pattern = 'libhfst_src/back-ends/foma/*.c'
foma_exclude = ('foma', 'iface', 'lex.cmatrix', 'lex.interface', 'stack')
foma_exclude_re = '/(?:' + '|'.join(re.escape(f) for f in foma_exclude) + r')\.cc?$'
foma_glob = [fname for fname in glob(foma_glob_pattern)
             if not re.search(foma_exclude_re, fname)]

# on windows, openfst back-end is in directory 'openfstwin'
if platform == 'win32':
    openfst_glob_pattern = 'libhfst_src/back-ends/openfstwin/src/lib/*.cc'
else:
    openfst_glob_pattern = 'libhfst_src/back-ends/openfst/src/lib/*.cc'
openfst_glob = glob(openfst_glob_pattern)

base_path = 'libhfst_src/libhfst/src/'
libhfst_glob = (glob(base_path + '*.cc')
                + glob(base_path + 'implementations/*.cc')
                + glob(base_path + 'implementations/compose_intersect/*.cc')
                + glob(base_path + 'implementations/optimized-lookup/*.cc')
                + glob(base_path + 'parsers/*.cc')
                + glob(base_path + 'parsers/alphabet_src/*.cc')
                + glob(base_path + 'parsers/io_src/*.cc')
                + glob(base_path + 'parsers/rule_src/*.cc')
                + glob(base_path + 'parsers/string_src/*.cc')
                + glob(base_path + 'parsers/variable_src/*.cc'))
libhfst_exclude = ('HfstXeroxRulesTest', 'ConvertSfstTransducer',
                   'ConvertXfsmTransducer', 'HfstTransitionGraph',
                   'MyTransducerLibraryTransducer', 'SfstTransducer',
                   'XfsmTransducer')
libhfst_exclude_re = '/(?:' + '|'.join(libhfst_exclude) + ')\.cc$'
libhfst_glob = [fname for fname in libhfst_glob
                if not re.search(libhfst_exclude_re, fname)]

libhfst_source_files = (libhfst_glob + foma_glob + openfst_glob)


package_data = {'hfst': []}
if platform == 'win32':
    if version_info >= (3, 4, 0):
        package_data['hfst'].extend(['MSVCP140.DLL', 'VCRUNTIME140.DLL'])

# ----- The HFST C++ EXTENSION -----

libhfst_module = Extension('hfst._libhfst',
                           language='c++',
                           sources=['src/hfst/libhfst.i'] + libhfst_source_files,
                           # swig-pre-generated source:
                           # sources=['src/hfst/libhfst_wrap.cpp'] + libhfst_source_files,
                           swig_opts=ext_swig_opts,
                           include_dirs=ext_include_dirs,
                           # library_dirs=[abs_libhfst_src_dir + '/.libs'],
                           libraries=['hfst'],
                           define_macros=ext_define_macros,
                           extra_compile_args=ext_extra_compile_args,
                           extra_link_args=ext_extra_link_args,
                           )

print('Extension arguments:')
pprint(libhfst_module.__dict__, stream=sys.stderr)

# NOTE: metadata taken from setup.cfg (setup.cfg overrides setup.py)
setup(ext_modules=[libhfst_module],
      package_data=package_data)
