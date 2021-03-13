#!/usr/bin/env python
"""Bump version number in VERSION based off the current HFST version and the
current version already uploaded to PyPI (or Test PyPI, if the --test flag is
given."""

import json
import re
import sys

import requests


print(f'Running {__file__} ...', file=sys.stderr)

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


def bump_python_version(hfst_version, pypi_version, test=False):
    new_version = '.'.join(str(v) for v in hfst_version)
    assert pypi_version[:3] <= hfst_version
    if pypi_version[:3] == hfst_version:
        new_version += f'.{int(pypi_version[3]) + 1}'
    else:
        new_version += '.0'
    if test:
        try:
            new_version += f'b{pypi_version[4] + 1}'
        except TypeError:
            new_version += 'b0'
    return new_version


def get_hfst_version():
    with open('libhfst_src/configure.ac') as f:
        configure_ac = f.read()
    major, minor, extension = re.search(r'LIBHFST_MAJOR=(\d+)\s*\n\s*LIBHFST_MINOR=(\d+)\s*\n\s*LIBHFST_EXTENSION=(\d+)', configure_ac).groups()
    hfst_version = (int(major), int(minor), int(extension))
    return hfst_version


def get_pypi_version(test=False):
    if not test:
        pypi_url = 'https://pypi.org/pypi/hfst/json'
    else:
        pypi_url = 'https://test.pypi.org/pypi/hfst/json'
    pypi_json = requests.get(pypi_url).text
    pypi_dict = json.loads(pypi_json)
    pypi_version = parse_python_pkg_version(pypi_dict['info']['version'])
    return pypi_version


hfst_version = get_hfst_version()
pypi_version = get_pypi_version(test=TEST)
new_version = bump_python_version(hfst_version, pypi_version, test=TEST)
print('HFST version:', hfst_version, file=sys.stderr)
print(f'Current {"Test " if TEST else ""}PyPI version:', pypi_version, file=sys.stderr)
print('New version:', new_version, file=sys.stderr)

path_to_VERSION = __file__.replace('scripts/bump_version.py', '') + 'VERSION'
with open(path_to_VERSION, 'w') as f:
    f.write(new_version)

print(f'VERSION updated to {new_version}.', file=sys.stderr)
print(new_version)
