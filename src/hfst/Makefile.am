# Copyright (c) 2016 University of Helsinki
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
# See the file COPYING included with this distribution for more
# information.

SWIG_INTERFACE = libhfst.i

BUILT_SOURCES = %_wrap.cpp.cpp

%_wrap.cpp.cpp: $(SWIG_INTERFACE) setup.py
	$(PYTHON) setup.py build

install-exec-local:
	$(PYTHON) setup.py install $(PYTHON_INSTALL_PARAMS)

SUBDIRS = test
EXTRA_DIST = libhfst.i docstrings.i README setup.py \
hfst_extensions.cpp hfst_file_extensions.cpp hfst_lexc_extensions.cpp hfst_sfst_extensions.cpp \
hfst_lookup_extensions.cpp hfst_pmatch_extensions.cpp hfst_prolog_extensions.cpp \
hfst_regex_extensions.cpp hfst_rules_extensions.cpp hfst_xfst_extensions.cpp \
hfst_pmatch_tokenize_extensions.cpp \
hfst/__init__.py hfst/exceptions/__init__.py hfst/sfst_rules/__init__.py \
hfst/xerox_rules/__init__.py

AUTOMAKE_OPTIONS = subdir-objects
