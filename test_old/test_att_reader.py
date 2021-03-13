# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst

transducers = []

with open('testfile.att', 'r') as f:
    r = hfst.AttReader(f, "<eps>")
    for tr in r:
        transducers.append(tr)

assert(f.closed)
assert(len(transducers)) == 4

transducers = []

with open('testfile_fail.att', 'r') as f:
    try:
        r = hfst.AttReader(f, "<eps>")
        for tr in r:
            transducers.append(tr)
    except hfst.exceptions.NotValidAttFormatException as e:
        assert("1      baz    baz      0.3" in e.what())
        assert("line: 11" in e.what())

assert(f.closed)
assert(len(transducers)) == 4

transducers = []
if sys.version_info[0] < 3:
    with open('testfile_unicode.att', 'rb') as f:
        r = hfst.AttReader(f)
        for tr in r:
            transducers.append(tr)
else:
    with open('testfile_unicode.att', 'r', encoding='utf-8') as f:
        r = hfst.AttReader(f)
        for tr in r:
            transducers.append(tr)

assert(f.closed)
assert(len(transducers)) == 1
TR = hfst.regex('föö:bär::0.5')
assert(TR.compare(transducers[0]))
