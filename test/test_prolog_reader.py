import os.path

import hfst

RSRC_DIR = os.path.dirname(__file__) + '/resources/'


def test_prolog_reader():
    transducers = []

    with open(RSRC_DIR + 'cats_and_dogs.prolog', 'r') as f:
        r = hfst.PrologReader(f)
        for tr in r:
            transducers.append(tr)

    assert f.closed
    assert len(transducers) == 4

    transducers = []

    with open(RSRC_DIR + 'cats_and_dogs_fail.prolog', 'r') as f:
        try:
            r = hfst.PrologReader(f)
            for tr in r:
                transducers.append(tr)
        except hfst.exceptions.NotValidPrologFormatException as e:
            assert 'arc(1, 2, "bar").' in e.what()
            assert 'line: 24' in e.what()

    assert f.closed
    assert len(transducers) == 4
