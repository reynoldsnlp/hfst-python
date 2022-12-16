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

from distutils.unixccompiler import UnixCCompiler
from glob import glob
import os
from pprint import pprint
import re
from setuptools.command.build_ext import build_ext
from setuptools import Extension
from setuptools import setup
from sys import platform
from sys import version_info


# default to 10.9, unless the environment variable is set to something else
MACOSX_VERSION_MIN = os.environ.get('MACOSX_DEPLOYMENT_TARGET', '10.9')

# Whether to use the C++ version of the foma back-end
FOMA_CPP = False

# ----- SWIG CONFIGURATION -----

# HFST C++ headers needed by swig when creating the python/c++ interface
abs_libhfst_src_dir = os.path.abspath('libhfst_src/libhfst/src/')

# Generate wrapper for C++
swig_opts = ['-c++', '-I' + abs_libhfst_src_dir, '-Wall']

# ----- LINKER ARGUMENTS -----

# Readline is needed for hfst.start_xfst(). On windows the shell where HFST
# python bindings are run from has its own readline which will do.
include_readline = False
include_getline = False
if platform.startswith('linux') or platform == 'darwin':
    include_readline = True
    include_getline = True
extra_link_args = []
if include_readline:
    extra_link_args = ['-lreadline']
if platform == 'darwin':
    extra_link_args.extend(['-mmacosx-version-min=' + MACOSX_VERSION_MIN])


# ----- INCLUDE DIRECTORIES -----

# HFST headers needed when compiling the actual c++ extension
include_dirs = [os.path.abspath('./libhfst_src'),  # config.h
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
    include_dirs.append(os.path.abspath('./libhfst_src/back-ends/foma/cpp-version'))
    # some headers are only in foma/
    include_dirs.append(os.path.abspath('./libhfst_src/back-ends/foma'))
else:
    include_dirs.append(os.path.abspath('./libhfst_src/back-ends/foma'))
if platform == 'win32':
    include_dirs.append(os.path.abspath('./libhfst_src/back-ends/dlfcn'))
    include_dirs.append(os.path.abspath('./libhfst_src/back-ends/openfstwin/src/include'))
    # include_dirs.append(os.path.abspath('./libhfst_src/back-ends/openfstwin/src/include/fst'))
else:
    include_dirs.append(os.path.abspath('./libhfst_src/back-ends/openfst/src/include'))
    # include_dirs.append(os.path.abspath('./libhfst_src/back-ends/openfst/src/include/fst'))


# -----  MACROS CONFIGURATION  -----

define_macros = []
define_macros.append(('HAVE_FOMA', None))
define_macros.append(('HAVE_OPENFST', None))
define_macros.append(('HAVE_OPENFST_LOG', None))

if include_readline:
    define_macros.append(('HAVE_READLINE', None))
if include_getline:
    define_macros.append(('HAVE_GETLINE', None))

# msvc-specific macros.
if platform == 'win32':
    # MSC_VER_ should already be defined
    for macro in ['HFSTEXPORT', 'OPENFSTEXPORT', 'WINDOWS', 'WIN32',
                  '_CRT_SECURE_NO_WARNINGS']:
        define_macros.append((macro, None))

# If C++11 is not supported, what features will be disabled and where unordered
# map and set are found.
# if platform == 'win32':
    # Disable c++11 features.
    # define_macros.append(('NO_CPLUSPLUS_11', None))
    # Unordered containers are in namespace std::tr1.
    # define_macros.append(('USE_TR1_UNORDERED_MAP_AND_SET', None))
    # On windows, the header files are not located in directory tr1
    # although the namespace is std::tr1.
#     if platform != 'win32':
#         define_macros.append(('INCLUDE_TR1_UNORDERED_MAP_AND_SET', None))


# ----- COMPILATION OPTIONS -----

extra_compile_args = []  # C and C++ flags
extra_cpp_args = []      # C++ flags

if platform == 'darwin' or platform.startswith('linux'):
    extra_compile_args.extend(['-Wno-sign-compare', '-Wno-strict-prototypes'])
    extra_cpp_args.extend(['-std=c++11'])

if platform == 'darwin':
    extra_cpp_args.extend(['-stdlib=libc++',
                           '-mmacosx-version-min=' + MACOSX_VERSION_MIN])
elif platform == 'win32':
    # define error handling mechanism on windows
    extra_compile_args = ['/EHsc']


# ----- C++ SOURCE FILES -----


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
libhfst_exclude_re = '/(?:' + '|'.join(libhfst_exclude) + r')\.cc$'
libhfst_glob = [fname for fname in libhfst_glob
                if not re.search(libhfst_exclude_re, fname)]

libhfst_src_files = (libhfst_glob + foma_glob + openfst_glob)


package_data = {'hfst': []}
if platform == 'win32':
    if version_info >= (3, 4, 0):
        package_data['hfst'].extend(['MSVCP140.DLL', 'VCRUNTIME140.DLL'])

# ----- The HFST C++ EXTENSION -----


class CCxxCompiler(UnixCCompiler):
    """User different flags for C and C++.

    Adapted from https://stackoverflow.com/a/65865696/2903532
    """
    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        if os.path.splitext(src)[-1] in ('.cpp', '.cxx', '.cc'):
            _cc_args = extra_cpp_args + cc_args
            try:
                _cc_args.remove('-Wno-strict-prototypes')
            except ValueError:
                pass
        else:
            _cc_args = cc_args
        UnixCCompiler._compile(self, obj, src, ext, _cc_args, extra_postargs,
                               pp_opts)


class BuildCCxxExtensions(build_ext):
    """Adapted from https://stackoverflow.com/a/65865696/2903532"""
    def build_extensions(self, ext):
        if self.compiler.compiler_type == 'unix':
            # Replace the compiler
            old_compiler = self.compiler
            self.compiler = CCxxCompiler()

            # Copy its attributes
            for attr, value in old_compiler.__dict__.items():
                setattr(self.compiler, attr, value)
        build_ext.build_extensions(self, ext)


libhfst_extension_kwargs = {'language': 'c++',
                            # sources: ['src/hfst/libhfst.i'] + libhfst_src_files,
                            # swig_opts: swig_opts,
                            # swig-pre-generated source:
                            'sources': ['src/hfst/libhfst_wrap.cpp'] + libhfst_src_files,
                            'include_dirs': include_dirs,
                            # 'library_dirs': [abs_libhfst_src_dir + '/.libs'],
                            # 'libraries': ['hfst'],
                            'define_macros': define_macros,
                            'extra_compile_args': extra_compile_args,
                            'extra_link_args': extra_link_args,
                            }
print('C++ extension arguments:')
pprint(libhfst_extension_kwargs)
_libhfst = Extension('hfst._libhfst', **libhfst_extension_kwargs)

# NOTE: metadata taken from setup.cfg (setup.cfg overrides setup.py)
setup(ext_modules=[_libhfst],
      package_data=package_data)
