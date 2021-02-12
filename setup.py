#!/usr/bin/python3

"""
Setup for creating PIP packages for HFST Python bindings.

Before running setup, make sure that the following C++ files
from 'hfst_src/libhfst/src/parsers' have been generated from flex/yacc files
before copying (on linux and OS X by running 'make' and on windows
with 'compile-parsers-win.sh' located in 'hfst_src/libhfst/src/parsers'):

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

import argparse
from glob import glob
import os
from pprint import pprint
from setuptools import Extension
from setuptools import setup
import sys
from sys import platform
from sys import version_info

MACOSX_VERSION_MIN = '10.9'

parser = argparse.ArgumentParser(description='Build hfst python module')

# # By default, use the C++ version of foma backend. C++11 requires option
# # -std=c++0x to be set for C/C++ compiler (this cannot de defined for each file
# # separately) and some compilers refuse to compile C with that option.
# foma_group = parser.add_mutually_exclusive_group()
# foma_group.add_argument('--with-c++-foma', action='store_const',
#                         dest='cpp_foma', const=True, default=True,
#                         help='Use C++ version of foma backend (default)')
# foma_group.add_argument('--with-c-foma', action='store_const', dest='cpp_foma',
#                         const=False, help='Use C version of foma backend')

wrapper_group = parser.add_mutually_exclusive_group()
wrapper_group.add_argument('--generate-wrapper', action='store_const',
                           dest='generate_wrapper', const=True, default=True,
                           help='Generate the SWIG wrapper (default)')
wrapper_group.add_argument('--no-generate-wrapper', action='store_const',
                           dest='generate_wrapper', const=False,
                           help='Do not generate SWIG wrapper.')

# local_group = parser.add_mutually_exclusive_group()
# local_group.add_argument('--local-hfst', action='store_const', dest='local',
#                          const=True, default=True,
#                          help='Link to local HFST library (default)')
# local_group.add_argument('--system-hfst', action='store_const', dest='local',
#                          const=False, help='Link to system HFST library.')


# parser.add_argument('--no-readline', action='store_true',
#                     help='Do not include readline')

args, unknown = parser.parse_known_args()
print(args, file=sys.stderr)
# remaining args are passed to setup using sys.argv
sys.argv = sys.argv[0:1] + unknown


def readme():
    with open('README.rst') as f:
        return f.read()


# Experimental...
if platform == 'darwin':
    os.environ['_PYTHON_HOST_PLATFORM'] = f'macosx-{MACOSX_VERSION_MIN}-x86_64'


# ----- SWIG CONFIGURATION -----

# HFST C++ headers needed by swig when creating the python/c++ interface
abs_libhfst_src_dir = os.path.abspath('hfst_src/libhfst/src/')

# Generate wrapper for C++
ext_swig_opts = ['-c++', '-I' + abs_libhfst_src_dir, '-Wall']

# By default, we build the wrapper
if args.generate_wrapper:
    ext_source = ['hfst/libhfst.i']
else:
    ext_source = ['hfst/libhfst_wrap.cpp']


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
    ext_extra_link_args.extend([f'-mmacosx-version-min={MACOSX_VERSION_MIN}'])
# if args.local:
#     ext_extra_link_args.extend([f'-Wl,-rpath,{abs_libhfst_src_dir}/.libs'])



# ----- INCLUDE DIRECTORIES -----

# HFST headers needed when compiling the actual c++ extension
ext_include_dirs = [os.path.abspath('hfst'),
                    os.path.abspath('hfst/lib'),  # TODO delete this line?
                    os.path.abspath('hfst_src/back-ends/foma'),
                    os.path.abspath('hfst_src/back-ends'),
                    os.path.abspath('hfst_src/libhfst/src/'),
                    os.path.abspath('hfst_src/libhfst/src/parsers'),
                    ]
if platform == 'win32':
    ext_include_dirs.append(os.path.abspath('hfst_src/back-ends/openfstwin/src/include'))
else:
    ext_include_dirs.append(os.path.abspath('hfst_src/back-ends/openfst/src/include'))


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
                                   f'-mmacosx-version-min={MACOSX_VERSION_MIN}'])
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
foma_src_dir = 'hfst_src/back-ends/foma/'
fe = cpp
# if not args.cpp_foma:
#     foma_src_dir = 'hfst_src/back-ends/foma/cpp-version/'
#     fe = '.c'

# all c++ extension source files

libhfst_source_files = glob('hfst_src/libhfst/src/parsers/*.c[cp]*')
# libhfst_source_files = ['hfst_src/libhfst/src/parsers/XfstCompiler' + cpp,
#                         'hfst_src/libhfst/src/HfstApply' + cpp,
#                         'hfst_src/libhfst/src/HfstInputStream' + cpp,
#                         'hfst_src/libhfst/src/HfstTransducer' + cpp,
#                         'hfst_src/libhfst/src/HfstOutputStream' + cpp,
#                         'hfst_src/libhfst/src/HfstRules' + cpp,
#                         'hfst_src/libhfst/src/HfstXeroxRules' + cpp,
#                         'hfst_src/libhfst/src/HfstDataTypes' + cpp,
#                         'hfst_src/libhfst/src/HfstSymbolDefs' + cpp,
#                         'hfst_src/libhfst/src/HfstTokenizer' + cpp,
#                         'hfst_src/libhfst/src/HfstFlagDiacritics' + cpp,
#                         'hfst_src/libhfst/src/HfstExceptionDefs' + cpp,
#                         'hfst_src/libhfst/src/HarmonizeUnknownAndIdentitySymbols' + cpp,
#                         'hfst_src/libhfst/src/HfstLookupFlagDiacritics' + cpp,
#                         'hfst_src/libhfst/src/HfstEpsilonHandler' + cpp,
#                         'hfst_src/libhfst/src/HfstStrings2FstTokenizer' + cpp,
#                         'hfst_src/libhfst/src/HfstPrintDot' + cpp,
#                         'hfst_src/libhfst/src/HfstPrintPCKimmo' + cpp,
#                         'hfst_src/libhfst/src/hfst-string-conversions' + cpp,
#                         'hfst_src/libhfst/src/string-utils' + cpp,
#                         'hfst_src/libhfst/src/implementations/HfstBasicTransducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/HfstBasicTransition' + cpp,
#                         'hfst_src/libhfst/src/implementations/ConvertTransducerFormat' + cpp,
#                         'hfst_src/libhfst/src/implementations/HfstTropicalTransducerTransitionData' + cpp,
#                         'hfst_src/libhfst/src/implementations/ConvertTropicalWeightTransducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/ConvertLogWeightTransducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/ConvertFomaTransducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/ConvertOlTransducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/TropicalWeightTransducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/LogWeightTransducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/FomaTransducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/HfstOlTransducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectRulePair' + cpp,
#                         'hfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectLexicon' + cpp,
#                         'hfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectRule' + cpp,
#                         'hfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectFst' + cpp,
#                         'hfst_src/libhfst/src/implementations/compose_intersect/ComposeIntersectUtilities' + cpp,
#                         'hfst_src/libhfst/src/implementations/optimized-lookup/transducer' + cpp,
#                         'hfst_src/libhfst/src/implementations/optimized-lookup/convert' + cpp,
#                         'hfst_src/libhfst/src/implementations/optimized-lookup/ospell' + cpp,
#                         'hfst_src/libhfst/src/implementations/optimized-lookup/pmatch' + cpp,
#                         'hfst_src/libhfst/src/implementations/optimized-lookup/pmatch_tokenize' + cpp,
#                         'hfst_src/libhfst/src/implementations/optimized-lookup/find_epsilon_loops' + cpp,
#                         'hfst_src/libhfst/src/parsers/xre_lex' + cpp,
#                         'hfst_src/libhfst/src/parsers/xre_parse' + cpp,
#                         'hfst_src/libhfst/src/parsers/pmatch_parse' + cpp,
#                         'hfst_src/libhfst/src/parsers/pmatch_lex' + cpp,
#                         'hfst_src/libhfst/src/parsers/lexc-parser' + cpp,
#                         'hfst_src/libhfst/src/parsers/lexc-lexer' + cpp,
#                         'hfst_src/libhfst/src/parsers/xfst-parser' + cpp,
#                         'hfst_src/libhfst/src/parsers/xfst-lexer' + cpp,
#                         'hfst_src/libhfst/src/parsers/LexcCompiler' + cpp,
#                         'hfst_src/libhfst/src/parsers/PmatchCompiler' + cpp,
#                         'hfst_src/libhfst/src/parsers/XreCompiler' + cpp,
#                         'hfst_src/libhfst/src/parsers/lexc-utils' + cpp,
#                         'hfst_src/libhfst/src/parsers/pmatch_utils' + cpp,
#                         'hfst_src/libhfst/src/parsers/xre_utils' + cpp,
#                         'hfst_src/libhfst/src/parsers/xfst-utils' + cpp,
#                         'hfst_src/libhfst/src/parsers/xfst_help_message' + cpp,
#                         'hfst_src/libhfst/src/parsers/sfst-scanner' + cpp,
#                         'hfst_src/libhfst/src/parsers/sfst-compiler' + cpp,
#                         'hfst_src/libhfst/src/parsers/SfstCompiler' + cpp,
#                         'hfst_src/libhfst/src/parsers/SfstAlphabet' + cpp,
#                         'hfst_src/libhfst/src/parsers/SfstBasic' + cpp,
#                         'hfst_src/libhfst/src/parsers/SfstUtf8' + cpp,
#                         'hfst_src/libhfst/src/parsers/htwolcpre1-lexer' + cpp,
#                         'hfst_src/libhfst/src/parsers/htwolcpre2-lexer' + cpp,
#                         'hfst_src/libhfst/src/parsers/htwolcpre3-lexer' + cpp,
#                         'hfst_src/libhfst/src/parsers/htwolcpre1-parser' + cpp,
#                         'hfst_src/libhfst/src/parsers/htwolcpre2-parser' + cpp,
#                         'hfst_src/libhfst/src/parsers/htwolcpre3-parser' + cpp,
#                         'hfst_src/libhfst/src/parsers/TwolcCompiler' + cpp,
#                         'hfst_src/libhfst/src/parsers/io_src/InputReader' + cpp,
#                         'hfst_src/libhfst/src/parsers/string_src/string_manipulation' + cpp,
#                         'hfst_src/libhfst/src/parsers/variable_src/RuleSymbolVector' + cpp,
#                         'hfst_src/libhfst/src/parsers/variable_src/RuleVariables' + cpp,
#                         'hfst_src/libhfst/src/parsers/variable_src/RuleVariablesConstIterator' + cpp,
#                         'hfst_src/libhfst/src/parsers/variable_src/VariableValues' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/ConflictResolvingLeftArrowRule' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/ConflictResolvingRightArrowRule' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/LeftArrowRule' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/LeftArrowRuleContainer' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/LeftRestrictionArrowRule' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/OtherSymbolTransducer' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/RightArrowRule' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/RightArrowRuleContainer' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/Rule' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/RuleContainer' + cpp,
#                         'hfst_src/libhfst/src/parsers/rule_src/TwolCGrammar' + cpp,
#                         'hfst_src/libhfst/src/parsers/alphabet_src/Alphabet' + cpp]

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

openfst_source_files = glob('hfst_src/back-ends/' + openfstdir + '/src/lib/compat.c[cp]*')
# openfst_source_files = ['hfst_src/back-ends/' + openfstdir + '/src/lib/compat' + cpp,
#                         'hfst_src/back-ends/' + openfstdir + '/src/lib/flags' + cpp,
#                         'hfst_src/back-ends/' + openfstdir + '/src/lib/fst' + cpp,
#                         'hfst_src/back-ends/' + openfstdir + '/src/lib/properties' + cpp,
#                         'hfst_src/back-ends/' + openfstdir + '/src/lib/symbol-table' + cpp,
#                         'hfst_src/back-ends/' + openfstdir + '/src/lib/symbol-table-ops' + cpp,
#                         'hfst_src/back-ends/' + openfstdir + '/src/lib/util' + cpp]

libhfst_source_files += openfst_source_files

if include_foma_backend:
    libhfst_source_files += foma_source_files

package_data = {'hfst': ['hfst/lib/*']}
if (platform == 'win32'):
    if (version_info[0] == 3 and version_info[1] > 4):
        package_data['hfst'].extend(['MSVCP140.DLL', 'VCRUNTIME140.DLL'])
    else:
        pass

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
                           sources=ext_source + libhfst_source_files,
                           swig_opts=ext_swig_opts,
                           include_dirs=ext_include_dirs,
                           library_dirs=[abs_libhfst_src_dir + '/.libs'],
                           libraries=['hfst'],
                           define_macros=ext_define_macros,
                           extra_compile_args=ext_extra_compile_args,
                           extra_link_args=ext_extra_link_args,
                           )

print('Extension arguments:', file=sys.stderr)
pprint(libhfst_module.__dict__, stream=sys.stderr)

setup(name='hfst',
      version='3.15.2.0',
      author='HFST team',
      author_email='hfst-bugs@helsinki.fi',
      url='http://hfst.github.io/',
      description='Python interface for HFST',
      long_description=readme(),
      long_description_content_type='text/x-rst',
      license='GNU GPL3',
      ext_modules=[libhfst_module],
      py_modules=['libhfst'],
      packages=['hfst', 'hfst.exceptions', 'hfst.sfst_rules',
                'hfst.xerox_rules'],
      package_data=package_data,
      include_package_data=True,
      data_files=[]
      )
