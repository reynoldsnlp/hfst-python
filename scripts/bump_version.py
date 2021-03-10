#!/usr/bin/env python
"""Bump version number in setup.py based off the current HFST version and the
current version already uploaded to PyPI (or Test PyPI, if the --test flag is
given."""

import json
import re
import sys

import requests


TEST = '--test' in sys.argv


def parse_python_pkg_version(input_str):
    print('Parsing python package version number', input_str, '...', file=sys.stderr)
    # Note that the b and the last digit are optional
    match = re.search(r'(\d+)\.(\d+)\.(\d+)\.(\d+)b?(\d*)', input_str)
    version = []
    for i in match.groups():
        try:
            version.append(int(i))
        except ValueError:
            version.append(None)
    return tuple(version)


def bump_python_version(HFST_version, pypi_version, test=False):
    new_version = '.'.join(str(v) for v in HFST_version)
    assert pypi_version[:3] <= HFST_version
    if pypi_version[:3] == HFST_version:
        new_version += f'.{int(pypi_version[3]) + 1}'
    else:
        new_version += '.0'
    if test:
        try:
            new_version += f'b{pypi_version[4] + 1}'
        except TypeError:
            new_version += 'b0'
    return new_version


def get_HFST_version():
    with open('hfst_src/configure.ac') as f:
        configure_ac = f.read()
    major, minor, extension = re.search(r'LIBHFST_MAJOR=(\d+)\s*\n\s*LIBHFST_MINOR=(\d+)\s*\n\s*LIBHFST_EXTENSION=(\d+)', configure_ac).groups()
    # print(major, minor, extension)  # Check hfst_src/configure.ac manually
    HFST_version = (int(major), int(minor), int(extension))
    return HFST_version


def get_pypi_version(test=False):
    if not test:
        pypi_url = 'https://pypi.org/pypi/hfst/json'
    else:
        pypi_url = 'https://test.pypi.org/pypi/hfst/json'
    pypi_json = requests.get(pypi_url).text
    pypi_dict = json.loads(pypi_json)
    pypi_version = parse_python_pkg_version(pypi_dict['info']['version'])
    return pypi_version


HFST_version = get_HFST_version()
pypi_version = get_pypi_version(test=TEST)
new_version = bump_python_version(HFST_version, pypi_version, test=TEST)
print('HFST version:', HFST_version, file=sys.stderr)
print(f'Current {"Test " if TEST else ""}PyPI version:', pypi_version, file=sys.stderr)
print('New version:', new_version, file=sys.stderr)

path_to_setup_py = __file__.replace('scripts/bump_version.py', '') + 'setup.py'
with open(path_to_setup_py) as f:
    setup_py = f.read()

setup_py = re.sub(r"version='.*?',  # automatically bumped by scripts/bump_version.py",
                  f"version='{new_version}',  # automatically bumped by scripts/bump_version.py",
                  setup_py)

with open(path_to_setup_py, 'w') as f:
    f.write(setup_py)

print('Version updated to the following version:', file=sys.stderr)
print(new_version)
print('Run the following to confirm:', file=sys.stderr)
print('git diff setup.py', file=sys.stderr)
