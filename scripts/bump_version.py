#!/usr/bin/env python3

"""
Bump version number in src/hfst/version.py based off the current HFST version
and the current version already uploaded to PyPI (or Test PyPI, if the --test
flag is given.
"""

import json
import re
import sys
import warnings

from packaging.version import parse
import requests


print(f'Running {__file__} ...', file=sys.stderr)

TEST = '--test' in sys.argv
BETA = '--beta' in sys.argv


def bump_python_version(hfst_version, pypi_version, beta=False):
    """Bump version.

    Parameters
    ----------
    hfst_version
        version of C++ hfst
    pypi_version
        latest version from PyPI
    beta
        If True, output beta version
    """
    pre = ''
    if hfst_version.release > pypi_version.release:
        base_version = list(hfst_version.release) + [0]
        if beta:
            pre = 'b0'
    else:
        base_version = list(pypi_version.release)
        if pypi_version.pre:  # if latest PyPI version is not beta
            if beta:
                pre = 'b' + str(pypi_version.pre[1] + 1)
        else:
            base_version[-1] += 1
            if beta:
                pre = 'b0'
    base_version = '.'.join(str(v) for v in base_version)
    return base_version + pre


def get_hfst_version():
    with open('libhfst_src/configure.ac') as f:
        configure_ac = f.read()
    github_configure_ac = requests.get('https://raw.githubusercontent.com/hfst/hfst/master/configure.ac').text
    version_re = r'LIBHFST_MAJOR=(\d+)\s*\n\s*LIBHFST_MINOR=(\d+)\s*\n\s*LIBHFST_EXTENSION=(\d+)'
    major, minor, extension = re.search(version_re, configure_ac).groups()
    gh_major, gh_minor, gh_extension = re.search(version_re, github_configure_ac).groups()
    hfst_version = (int(major), int(minor), int(extension))
    github_version = (int(gh_major), int(gh_minor), int(gh_extension))
    if github_version > hfst_version:
        warnings.warn('WARNING: HFST master branch has newer version. Run `git submodule update --recursive`.')
        response = input('Continue anyway? (y/N) ')
        if response not in {'Y', 'y'}:
            sys.exit(1)
    return parse('.'.join(str(i) for i in hfst_version))


def get_pypi_version(test=False):
    """Get version from PyPI json

    test -- if True, use test.pypi.org
    """
    if test:
        pypi_url = 'https://test.pypi.org/pypi/hfst/json'
    else:
        pypi_url = 'https://pypi.org/pypi/hfst/json'
    pypi_json = requests.get(pypi_url).text
    pypi_dict = json.loads(pypi_json)
    releases = [parse(version)
                for version in pypi_dict['releases']]
    latest_release = sorted(releases)[-1]
    return latest_release


def tests():
    hv = parse('1.2.3')
    for t, expected in [('1.2.2.5', '1.2.3.0'),
                        ('1.2.2.5b4', '1.2.3.0'),
                        ('1.2.3.0', '1.2.3.1'),
                        ('1.2.3.0b4', '1.2.3.0'),
                        ('1.2.3.1', '1.2.3.2'),
                        ('1.2.3.1b4', '1.2.3.1')]:
        print('1.2.3', t, bump_python_version(hv, parse(t)), sep='\t')
        assert bump_python_version(hv, parse(t), beta=False) == expected, ('1.2.3', t, expected)
    print('BETA')
    for t, expected in [('1.2.2.5', '1.2.3.0b0'),
                        ('1.2.2.5b4', '1.2.3.0b0'),
                        ('1.2.3.0', '1.2.3.1b0'),
                        ('1.2.3.0b4', '1.2.3.0b5'),
                        ('1.2.3.1', '1.2.3.2b0'),
                        ('1.2.3.1b4', '1.2.3.1b5')]:
        print('1.2.3', t, bump_python_version(hv, parse(t), beta=True), sep='\t')
        assert bump_python_version(hv, parse(t), beta=True) == expected, ('1.2.3', t, expected)


def write_version_files(new_version):
    base_dir = __file__.replace('scripts/bump_version.py', '')

    path_to_version_py = base_dir + 'src/hfst/version.py'
    with open(path_to_version_py, 'w') as f:
        print(f'''version = "{new_version}"''', file=f)

    print(f'src/hfst/version.py updated to {new_version}.', file=sys.stderr)


if __name__ == '__main__':
    hfst_version = get_hfst_version()
    pypi_version = get_pypi_version(test=TEST)
    new_version = bump_python_version(hfst_version, pypi_version, beta=BETA)
    print('HFST version:', hfst_version, file=sys.stderr)
    print(f'Current {"Test " if TEST else ""}PyPI version:', pypi_version, file=sys.stderr)
    print('New version:', new_version, file=sys.stderr)
    write_version_files(new_version)

    print(new_version)
