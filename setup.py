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

# import argparse
from glob import glob
import os
from pprint import pprint
from setuptools import Extension
from setuptools import setup
import sys
from sys import platform
from sys import version_info

# default to 10.9, unless the environment variable is set to something else
MACOSX_VERSION_MIN = os.environ.get('MACOSX_DEPLOYMENT_TARGET', '10.9')

# parser = argparse.ArgumentParser(description='Build hfst python module')

# # By default, use the C++ version of foma backend. C++11 requires option
# # -std=c++0x to be set for C/C++ compiler (this cannot de defined for each file
# # separately) and some compilers refuse to compile C with that option.
# foma_group = parser.add_mutually_exclusive_group()
# foma_group.add_argument('--with-c++-foma', action='store_const',
#                         dest='cpp_foma', const=True, default=True,
#                         help='Use C++ version of foma backend (default)')
# foma_group.add_argument('--with-c-foma', action='store_const', dest='cpp_foma',
#                         const=False, help='Use C version of foma backend')

# wrapper_group = parser.add_mutually_exclusive_group()
# wrapper_group.add_argument('--generate-wrapper', action='store_const',
#                            dest='generate_wrapper', const=True, default=True,
#                            help='Generate the SWIG wrapper (default)')
# wrapper_group.add_argument('--no-generate-wrapper', action='store_const',
#                            dest='generate_wrapper', const=False,
#                            help='Do not generate SWIG wrapper.')

# local_group = parser.add_mutually_exclusive_group()
# local_group.add_argument('--local-hfst', action='store_const', dest='local',
#                          const=True, default=True,
#                          help='Link to local HFST library (default)')
# local_group.add_argument('--system-hfst', action='store_const', dest='local',
#                          const=False, help='Link to system HFST library.')


# parser.add_argument('--no-readline', action='store_true',
#                     help='Do not include readline')

# args, unknown = parser.parse_known_args()
# print(args, file=sys.stderr)
# remaining args are passed to setup using sys.argv
# sys.argv = sys.argv[0:1] + unknown


# def readme():
#     with open('README.rst') as f:
#         return f.read()


# def version():
#     with open('VERSION') as f:
#         return f.read().strip()


# ----- SWIG CONFIGURATION -----

# HFST C++ headers needed by swig when creating the python/c++ interface
abs_libhfst_src_dir = os.path.abspath('libhfst_src/libhfst/src/')

# Generate wrapper for C++
ext_swig_opts = ['-c++', '-I' + abs_libhfst_src_dir, '-Wall']

# By default, we build the wrapper
# if args.generate_wrapper:
#     ext_source = ['src/hfst/libhfst.i']
# else:
#     ext_source = ['src/hfst/libhfst_wrap.cpp']


# ----- LINKER ARGUMENTS -----

# Readline is needed for hfst.start_xfst(). On windows the shell where HFST
# python bindings are run from has its own readline which will do.
include_readline = False
include_getline = False
if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
    include_readline = True
    include_getline = True
# if args.no_readline:
#     include_readline = False
ext_extra_link_args = []
if include_readline:
    ext_extra_link_args = ['-lreadline']
# Experimental...
if platform == 'darwin':
    ext_extra_link_args.extend(['-mmacosx-version-min=' + MACOSX_VERSION_MIN])
# if args.local:
#     ext_extra_link_args.extend(['-Wl,-rpath,' + abs_libhfst_src_dir + '/.libs'])


# ----- INCLUDE DIRECTORIES -----

# HFST headers needed when compiling the actual c++ extension
ext_include_dirs = [os.path.abspath('src/hfst'),
                    os.path.abspath('src/hfst/lib'),  # TODO delete this line?
                    os.path.abspath('libhfst_src/back-ends/foma'),
                    os.path.abspath('libhfst_src/back-ends'),
                    os.path.abspath('libhfst_src/libhfst/src/'),
                    os.path.abspath('libhfst_src/libhfst/src/parsers'),
                    ]
if platform == 'win32':
    ext_include_dirs.append(os.path.abspath('libhfst_src/back-ends/openfstwin/src/include'))
else:
    ext_include_dirs.append(os.path.abspath('libhfst_src/back-ends/openfst/src/include'))


# ----- CONFIGURATION -----

ext_define_macros = []

# TODO ??
# Include foma implementation for OS X only when c++11 is disabled.
ext_define_macros.append(('HAVE_FOMA', None))

# Openfst backend is always enabled
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
if platform != 'darwin':
    # Disable c++11 features.
    ext_define_macros.append(('NO_CPLUSPLUS_11', None))
    # Unordered containers are in namespace std::tr1.
    ext_define_macros.append(('USE_TR1_UNORDERED_MAP_AND_SET', None))
    # On windows, the header files are not located in directory tr1
    # although the namespace is std::tr1.
    if platform != 'win32':
        ext_define_macros.append(('INCLUDE_TR1_UNORDERED_MAP_AND_SET', None))


# ----- COMPILATION OPTIONS -----

ext_extra_compile_args = []
if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
    ext_extra_compile_args = ['-Wno-sign-compare', '-Wno-strict-prototypes']
    # C++11 standard does not need to be specifically requested for msvc compilers.
    if platform == 'darwin':
        ext_extra_compile_args.extend(['-std=c++0x'])
# Experimental...
if platform == 'darwin':
    ext_extra_compile_args.extend(['-stdlib=libc++',
                                   '-mmacosx-version-min=' + MACOSX_VERSION_MIN])
# define error handling mechanism on windows
if platform == 'win32':
    ext_extra_compile_args = ['/EHsc']


# ----- C++ SOURCE FILES -----

# C++ source files have 'cpp' extension
cpp = '.cpp'

# on windows, openfst back-end is in directory 'openfstwin'
openfstdir = 'openfst'
if platform == 'win32':
    openfstdir = 'openfstwin'

# foma source file extension (C++ by default)
foma_src_dir = 'libhfst_src/back-ends/foma/'
fe = cpp
# if not args.cpp_foma:
#     foma_src_dir = 'libhfst_src/back-ends/foma/cpp-version/'
#     fe = '.c'

# all c++ extension source files

libhfst_source_files = glob('libhfst_src/libhfst/src/parsers/*.c[cp]*')
# libhfst_source_files = ['libhfst_src/libhfst/src/parsers/XfstCompiler' + cpp,
#                         'libhfst_src/libhfst/src/HfstApply' + cpp,
#                         'libhfst_src/libhfst/src/HfstInputStream' + cpp,
#                         'libhfst_src/libhfst/src/HfstTransducer' + cpp,
#                         'libhfst_src/libhfst/src/HfstOutputStream' + cpp,
#                         'libhfst_src/libhfst/src/HfstRules' + cpp,
#                         'libhfst_src/libhfst/src/HfstXeroxRules' + cpp,
#                         'libhfst_src/libhfst/src/HfstDataTypes' + cpp,
#                         'libhfst_src/libhfst/src/HfstSymbolDefs' + cpp,
#                         'libhfst_src/libhfst/src/HfstTokenizer' + cpp,
#                         'libhfst_src/libhfst/src/HfstFlagDiacritics' + cpp,
#                         'libhfst_src/libhfst/src/HfstExceptionDefs' + cpp,
#                         'libhfst_src/libhfst/src/HarmonizeUnknownAndIdentitySymbols' + cpp,
#                         'libhfst_src/libhfst/src/HfstLookupFlagDiacritics' + cpp,
#                         'libhfst_src/libhfst/src/HfstEpsilonHandler' + cpp,
#                         'libhfst_src/libhfst/src/HfstStrings2FstTokenizer' + cpp,
#                         'libhfst_src/libhfst/src/HfstPrintDot' + cpp,
#                         'libhfst_src/libhfst/src/HfstPrintPCKimmo' + cpp,
#                         'libhfst_src/libhfst/src/hfst-string-conversions' + cpp,
#                         'libhfst_src/libhfst/src/string-utils' + cpp,
#                         'libhfst_src/libhfst/src/implementations/HfstBasicTransducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/HfstBasicTransition' + cpp,
#                         'libhfst_src/libhfst/src/implementations/ConvertTransducerFormat' + cpp,
#                         'libhfst_src/libhfst/src/implementations/HfstTropicalTransducerTransitionData' + cpp,
#                         'libhfst_src/libhfst/src/implementations/ConvertTropicalWeightTransducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/ConvertLogWeightTransducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/ConvertFomaTransducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/ConvertOlTransducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/TropicalWeightTransducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/LogWeightTransducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/FomaTransducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/HfstOlTransducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectRulePair' + cpp,
#                         'libhfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectLexicon' + cpp,
#                         'libhfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectRule' + cpp,
#                         'libhfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectFst' + cpp,
#                         'libhfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectUtilities' + cpp,
#                         'libhfst_src/libhfst/src/implementations/optimized-lookup/transducer' + cpp,
#                         'libhfst_src/libhfst/src/implementations/optimized-lookup/convert' + cpp,
#                         'libhfst_src/libhfst/src/implementations/optimized-lookup/ospell' + cpp,
#                         'libhfst_src/libhfst/src/implementations/optimized-lookup/pmatch' + cpp,
#                         'libhfst_src/libhfst/src/implementations/optimized-lookup/pmatch_tokenize' + cpp,
#                         'libhfst_src/libhfst/src/implementations/optimized-lookup/find_epsilon_loops' + cpp,
#                         'libhfst_src/libhfst/src/parsers/xre_lex' + cpp,
#                         'libhfst_src/libhfst/src/parsers/xre_parse' + cpp,
#                         'libhfst_src/libhfst/src/parsers/pmatch_parse' + cpp,
#                         'libhfst_src/libhfst/src/parsers/pmatch_lex' + cpp,
#                         'libhfst_src/libhfst/src/parsers/lexc-parser' + cpp,
#                         'libhfst_src/libhfst/src/parsers/lexc-lexer' + cpp,
#                         'libhfst_src/libhfst/src/parsers/xfst-parser' + cpp,
#                         'libhfst_src/libhfst/src/parsers/xfst-lexer' + cpp,
#                         'libhfst_src/libhfst/src/parsers/LexcCompiler' + cpp,
#                         'libhfst_src/libhfst/src/parsers/PmatchCompiler' + cpp,
#                         'libhfst_src/libhfst/src/parsers/XreCompiler' + cpp,
#                         'libhfst_src/libhfst/src/parsers/lexc-utils' + cpp,
#                         'libhfst_src/libhfst/src/parsers/pmatch_utils' + cpp,
#                         'libhfst_src/libhfst/src/parsers/xre_utils' + cpp,
#                         'libhfst_src/libhfst/src/parsers/xfst-utils' + cpp,
#                         'libhfst_src/libhfst/src/parsers/xfst_help_message' + cpp,
#                         'libhfst_src/libhfst/src/parsers/sfst-scanner' + cpp,
#                         'libhfst_src/libhfst/src/parsers/sfst-compiler' + cpp,
#                         'libhfst_src/libhfst/src/parsers/SfstCompiler' + cpp,
#                         'libhfst_src/libhfst/src/parsers/SfstAlphabet' + cpp,
#                         'libhfst_src/libhfst/src/parsers/SfstBasic' + cpp,
#                         'libhfst_src/libhfst/src/parsers/SfstUtf8' + cpp,
#                         'libhfst_src/libhfst/src/parsers/htwolcpre1-lexer' + cpp,
#                         'libhfst_src/libhfst/src/parsers/htwolcpre2-lexer' + cpp,
#                         'libhfst_src/libhfst/src/parsers/htwolcpre3-lexer' + cpp,
#                         'libhfst_src/libhfst/src/parsers/htwolcpre1-parser' + cpp,
#                         'libhfst_src/libhfst/src/parsers/htwolcpre2-parser' + cpp,
#                         'libhfst_src/libhfst/src/parsers/htwolcpre3-parser' + cpp,
#                         'libhfst_src/libhfst/src/parsers/TwolcCompiler' + cpp,
#                         'libhfst_src/libhfst/src/parsers/io_src/InputReader' + cpp,
#                         'libhfst_src/libhfst/src/parsers/string_src/string_manipulation' + cpp,
#                         'libhfst_src/libhfst/src/parsers/variable_src/RuleSymbolVector' + cpp,
#                         'libhfst_src/libhfst/src/parsers/variable_src/RuleVariables' + cpp,
#                         'libhfst_src/libhfst/src/parsers/variable_src/RuleVariablesConstIterator' + cpp,
#                         'libhfst_src/libhfst/src/parsers/variable_src/VariableValues' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/ConflictResolvingLeftArrowRule' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/ConflictResolvingRightArrowRule' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/LeftArrowRule' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/LeftArrowRuleContainer' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/LeftRestrictionArrowRule' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/OtherSymbolTransducer' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/RightArrowRule' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/RightArrowRuleContainer' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/Rule' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/RuleContainer' + cpp,
#                         'libhfst_src/libhfst/src/parsers/rule_src/TwolCGrammar' + cpp,
#                         'libhfst_src/libhfst/src/parsers/alphabet_src/Alphabet' + cpp]

foma_source_files = glob(foma_src_dir + '*.c[cp]*')
# foma_source_files = [foma_src_dir + 'int_stack' + fe,
#                      foma_src_dir + 'define' + fe,
#                      foma_src_dir + 'determinize' + fe,
#                      foma_src_dir + 'apply' + fe,
#                      foma_src_dir + 'rewrite' + fe,
#                      foma_src_dir + 'topsort' + fe,
#                      foma_src_dir + 'flags' + fe,
#                      foma_src_dir + 'minimize' + fe,
#                      foma_src_dir + 'reverse' + fe,
#                      foma_src_dir + 'extract' + fe,
#                      foma_src_dir + 'sigma' + fe,
#                      foma_src_dir + 'structures' + fe,
#                      foma_src_dir + 'constructions' + fe,
#                      foma_src_dir + 'coaccessible' + fe,
#                      foma_src_dir + 'io' + fe,
#                      foma_src_dir + 'utf8' + fe,
#                      foma_src_dir + 'spelling' + fe,
#                      foma_src_dir + 'dynarray' + fe,
#                      foma_src_dir + 'mem' + fe,
#                      foma_src_dir + 'stringhash' + fe,
#                      foma_src_dir + 'trie' + fe,
#                      foma_src_dir + 'lex.yy' + fe,
#                      foma_src_dir + 'regex' + fe]

openfst_source_files = glob('libhfst_src/back-ends/' + openfstdir + '/src/lib/compat.c[cp]*')
# openfst_source_files = ['libhfst_src/back-ends/' + openfstdir + '/src/lib/compat' + cpp,
#                         'libhfst_src/back-ends/' + openfstdir + '/src/lib/flags' + cpp,
#                         'libhfst_src/back-ends/' + openfstdir + '/src/lib/fst' + cpp,
#                         'libhfst_src/back-ends/' + openfstdir + '/src/lib/properties' + cpp,
#                         'libhfst_src/back-ends/' + openfstdir + '/src/lib/symbol-table' + cpp,
#                         'libhfst_src/back-ends/' + openfstdir + '/src/lib/symbol-table-ops' + cpp,
#                         'libhfst_src/back-ends/' + openfstdir + '/src/lib/util' + cpp]

libhfst_source_files += openfst_source_files
libhfst_source_files += foma_source_files

package_data = {'hfst': []}
if platform == 'win32':
    if version_info >= (3, 4, 0):
        package_data['hfst'].extend(['MSVCP140.DLL', 'VCRUNTIME140.DLL'])

# (Is this needed?)
# foma_object_files = []
# (compile foma backend separately)
# for file in back-ends/foma/*.c; do clang -fPIC -std=c99 -arch i386 -arch
# x86_64 -mmacosx-version-min=10.9 -DHAVE_FOMA -c $file ; done
# if platform == 'darwin':
#     for file in foma_source_files:
#         foma_object_files.append(file.replace('back-ends/foma/','').replace('.c','.o'))
# in Extension: extra_objects = foma_object_files


# ----- The HFST C++ EXTENSION -----

libhfst_module = Extension('hfst._libhfst',
                           language='c++',
                           sources=['src/hfst/libhfst.i'] + libhfst_source_files,
                           swig_opts=ext_swig_opts,
                           include_dirs=ext_include_dirs,
                           library_dirs=[abs_libhfst_src_dir + '/.libs'],
                           libraries=['hfst'],
                           define_macros=ext_define_macros,
                           extra_compile_args=ext_extra_compile_args,
                           extra_link_args=ext_extra_link_args,
                           )

print('Extension arguments:')
pprint(libhfst_module.__dict__, stream=sys.stderr)

# NOTE: metadata taken from setup.cfg (setup.cfg overrides setup.py)
setup(ext_modules=[libhfst_module],
      py_modules=['libhfst'],
      # packages=['hfst', 'hfst.exceptions', 'hfst.sfst_rules',
      #           'hfst.xerox_rules'],
      package_data=package_data,
      include_package_data=True
      )
