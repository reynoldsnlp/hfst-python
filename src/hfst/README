
This folder contains source code for SWIG bindings for using HFST library with
Python. The bindings work with Python version 2.7 and from version 3.4 upwards.

============
REQUIREMENTS
============

The requirements for HFST C++ library are given in README of parent directory.
Compiling the bindings requires swig (tested with version 3.0.12) and
distutils (tested with version 36.0.1) as well as a C++ compiler (tested with
gcc 5.4.0).

=====================
BUILDING THE BINDINGS
=====================

Building and installation is done using the standard Python module distutils.
Once you've successfully built and installed HFST library (located in the
parent directory, if you are compiling from source), use the script setup.py
to build the Python extension eg. like so:

    python setup.py build_ext --inplace

If you have only built HFST library but not installed it (or have an earlier
version of HFST library installed) and want to build the bindings, running

    python setup.py build_ext --inplace --local-hfst

will link to the HFST library located in ../libhfst/src.


=================
RUNNING THE TESTS
=================

The folder 'test' contains tests for the bindings. See test/README for more
information.


=======================
INSTALLING THE BINDINGS
=======================

If you wish to install the extension, run

    python setup.py install

The same that was said about linking to HFST C++ library in 'Building the
bindings' above, applies also to installing.


For further information, consult

    python setup.py --help
    python setup.py --help-commands

and the distutils documentation.


==================
USING THE BINDINGS
==================

The bindings should be usable after installation in Python with command:

  import hfst

NOTE: If you want to use Python bindings locally, either add the absolute path
to this folder to PYTHONPATH, e.g. by executing

    PYTHONPATH="path/to/hfst-top-dir/python:"$PYTHONPATH

or do the following in Python before importing hfst:

    import sys
    sys.path.insert(1, 'path/to/hfst-top-dir/python')


====================
THE PYTHON INTERFACE
====================

C++ side functions and classes are wrapped with SWIG under module 'libhfst'. It
is possible to use this module directly, but there is a package named 'hfst'
which encapsulates the libhfst module in a more user-friendly manner. The
structure of the package is

 * hfst
    * hfst.exceptions
    * hfst.sfst_rules
    * hfst.xerox_rules

The module hfst.exceptions contains HfstException and its subclasses. The
modules hfst.sfst_rules and hfst.xerox_rules contain functions that create
transducers implementing replace and two-level rules. All other functions and
classes are in module hfst.

For documentation and examples, see <https://hfst.github.io/python/index.html>.


==========
KNOWN BUGS
==========

Some version combinations of SWIG and Python make HFST exception classes
subclasses of Python's _object instead of Exception. Then you will get an
error like

    TypeError: catching classes that do not inherit from BaseException is not allowed

If this is the case, run

    sed -i 's/class HfstException(_object):/class HfstException(Exception):/' libhfst.py

after build/installation to be able to use HfstException and its subclasses in
Python.
