# HFST for python

| | |
| --- | --- |
| CI/CD | [![CI - Test, Build, and Publish](https://github.com/reynoldsnlp/hfst-python/actions/workflows/build.yml/badge.svg)](https://github.com/reynoldsnlp/hfst-python/actions/workflows/build.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/hfst.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/hfst/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/hfst.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/hfst/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hfst.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/hfst/) |
| Meta | ![CI Buildwheel Badge](https://img.shields.io/badge/build-cibuildwheel-blue?logo=python&link=https%3A%2F%2Fcibuildwheel.readthedocs.io%2Fen%2Fstable%2F) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff) ![PyPI - License](https://img.shields.io/pypi/l/hfst) |

## Package description

Package `hfst` contains python bindings for the [Helsinki Finite-State
Technology (HFST)](https://hfst.github.io) C++ library. HFST toolkit is
intended for processing natural language morphologies. The toolkit is
demonstrated by wide-coverage implementations of a number of languages of
varying morphological complexity.

## Installation

For most users, simply run...

```console
$ python3 -m pip install hfst
```

On some OSes, you can install `hfst` python bindings by [running
`install_nightly.sh`](https://wiki.apertium.org/wiki/Installation#Install_Apertium_Core_by_packaging.2Fvirtual_environment).


We compile wheels using
[cibuildwheel](https://cibuildwheel.readthedocs.io/en/stable/) which enables us
to publish wheels for CPython and PyPy on a large variety of OS/architecture
combinations.  If wheels for your platform are not available, open an issue!
(Windows support coming soon!)

## Usage

C++ side functions and classes are wrapped with SWIG under module 'libhfst'. It
is possible to use this module directly, but there is a package named 'hfst'
which encapsulates the libhfst module in a more user-friendly manner. The
structure of the package is

* hfst
  * hfst.exceptions
  * hfst.sfst\_rules
  * hfst.xerox\_rules

The module hfst.exceptions contains HfstException and its subclasses. The
modules hfst.sfst\_rules and hfst.xerox\_rules contain functions that create
transducers implementing replace and two-level rules. All other functions and
classes are in module hfst.

For documentation and examples, see https://hfst.github.io/python/index.html.

## Requirements

Compiling hfst from source requires at least C++ compiler (tested with gcc 5.4.0),
readline and getline libraries and setuptools package for python
(tested with version 28.8.0). Swig is no longer needed as pre-generated files are
included in source distribution.

## Compiling from scratch

This repository has a submodule with the underlying C++ code. The first time
you clone this repository, run `$ git submodule init` to initialize the
submodule. Thereafter, every time that you want to pull in the latest changes
from the C++ hfst repository, run `$ git submodule update --remote` or `$ git
pull --recurse-submodules`. See the [manylinux build
script](scripts/linux_before_all.sh) for an example of how to compile the
underlying C++ library.

Once the library is available, the package can be installed by running...

```
python3 -m pip install .
```

...in the root directory of the repository.

## Running tests

Tests are contained in the `test/` directory. To run tests, you must first
install `pytest` using `python3 -m pip install pytest`.  Then, in the
root directory of this repository, run `python3 -m pytest`.

## Documentation

See wiki-based [package documentation](https://github.com/hfst/python/wiki) on
our Github pages. In python, you can also use `dir` and `help` commands, e.g.:

``dir(hfst)``

``help(hfst.HfstTransducer)``

## License

HFST is licensed under Gnu GPL version 3.0.

## Troubleshooting

#### *Pip starts to compile from source although there is a wheel available*

Try upgrading pip with

```
python3 -m pip install --upgrade pip
```

Another reason for this can be that the source package on PyPI is newer (i.e.
has a higher version number) than the corresponding wheel for the given
environment. Report this via our [issue
tracker](https://github.com/reynoldsnlp/hfst-python/issues/) so a fresh wheel
can be created.

#### *Error message "command ... failed with error code ..."*

Try rerunning pip in verbose mode with

```
python3 -m pip install --verbose [--upgrade] hfst
```

to get more information.

#### TypeError: catching classes that do not inherit from BaseException is not allowed

Some version combinations of SWIG and Python make HFST exception classes
subclasses of Python's `object` instead of Exception. Then you will get the
error above. If this is the case, run...

```
sed -i 's/class HfstException(_object):/class HfstException(Exception):/' libhfst.py
```

...after build/installation to be able to use HfstException and its subclasses in
Python.

## Links

[HFST project main page](https://hfst.github.io): more information about the
project

[Github issue tracker](https://github.com/hfst/hfst/issues/): for comments,
feature requests and bug reports
