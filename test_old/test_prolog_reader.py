# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst

transducers = []

with open('cats_and_dogs.prolog', 'r') as f:
    r = hfst.PrologReader(f)
    for tr in r:
        transducers.append(tr)

assert(f.closed)
assert(len(transducers)) == 4

transducers = []

with open('cats_and_dogs_fail.prolog', 'r') as f:
    try:
        r = hfst.PrologReader(f)
        for tr in r:
            transducers.append(tr)
    except hfst.exceptions.NotValidPrologFormatException as e:
        assert 'arc(1, 2, "bar").' in e.what()
        assert 'line: 24' in e.what()

assert(f.closed)
assert(len(transducers)) == 4
