import os.path

import hfst

RSRC_DIR = os.path.dirname(__file__) + '/resources/'


def test_att_reader1():
    transducers = []

    with open(RSRC_DIR + 'testfile.att', 'r') as f:
        r = hfst.AttReader(f, "<eps>")
        for tr in r:
            transducers.append(tr)

    assert(f.closed)
    assert(len(transducers)) == 4


def test_att_reader2():
    transducers = []

    with open(RSRC_DIR + 'testfile_fail.att', 'r') as f:
        try:
            r = hfst.AttReader(f, "<eps>")
            for tr in r:
                transducers.append(tr)
        except hfst.exceptions.NotValidAttFormatException as e:
            assert("1      baz    baz      0.3" in e.what())
            assert("line: 11" in e.what())

    assert(f.closed)
    assert(len(transducers)) == 4


def test_att_reader3():
    transducers = []
    with open(RSRC_DIR + 'testfile_unicode.att', 'r', encoding='utf-8') as f:
        r = hfst.AttReader(f)
        for tr in r:
            transducers.append(tr)

    assert(f.closed)
    assert(len(transducers)) == 1
    TR = hfst.regex('föö:bär::0.5')
    assert(TR.compare(transducers[0]))
