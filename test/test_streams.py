import hfst


def write_tr(fname):
    tr1 = hfst.regex('föö:bär')
    tr2 = hfst.regex('0')
    tr3 = hfst.regex('0-0')

    ostr = hfst.HfstOutputStream(filename=fname)
    ostr.write(tr1)
    ostr.write(tr2)
    ostr.write(tr3)
    ostr.flush()
    ostr.close()


def read_tr_and_write_att(fname1, fname2):
    transducers = []
    istr = hfst.HfstInputStream(fname1)
    while not istr.is_eof():
        transducers.append(istr.read())
    istr.close()

    assert len(transducers) == 3, 'Wrong number of transducers read.'

    for expr, tr in zip(['föö:bär', '0', '0-0'], transducers):
        assert tr.compare(hfst.regex(expr)), 'Transducers are not equivalent.'

    with open(fname2, 'w') as f:
        for i, tr in enumerate(transducers):
            tr.write_att(f)
            if i < len(transducers) - 1:
                f.write('--\n')


def read_att(fname2):
    transducers = []

    with open(fname2) as f:
        while True:
            try:
                transducers.append(hfst.read_att_transducer(f))
            except hfst.exceptions.EndOfStreamException:
                break

    assert len(transducers) == 3, 'Wrong number of transducers read.'

    for re, tr in zip(['föö:bär', '0', '0-0'], transducers):
        assert tr.compare(hfst.regex(re)), 'Transducers are not equivalent.'


def write_tr_ALL(fname):
    tr1 = hfst.regex('föö:bär')
    tr2 = hfst.regex('0')
    tr3 = hfst.regex('0-0')
    trs = [tr1, tr2, tr3]

    ostr = hfst.HfstOutputStream(filename=fname)
    ostr.write(trs)
    ostr.flush()
    ostr.close()


def read_tr_ALL(fname):
    istr = hfst.HfstInputStream(fname)
    transducers = istr.read_all()
    istr.close()

    assert len(transducers) == 3, 'Wrong number of transducers read.'

    for expr, tr in zip(['föö:bär', '0', '0-0'], transducers):
        assert tr.compare(hfst.regex(expr)), 'Transducers are not equivalent.'


def run_tests(path):
    fname1 = str(path / 'test_streams1.hfst')
    fname2 = str(path / 'test_streams2.hfst')
    fname3 = str(path / 'test_streams3.hfst')

    write_tr(fname1)
    read_tr_and_write_att(fname1, fname2)
    read_att(fname2)

    write_tr_ALL(fname3)
    read_tr_ALL(fname3)


def test_streams_foma(tmp_path):
    hfst.set_default_fst_type(hfst.ImplementationType.FOMA_TYPE)
    run_tests(tmp_path)


def test_streams_openfst(tmp_path):
    hfst.set_default_fst_type(hfst.ImplementationType.TROPICAL_OPENFST_TYPE)
    run_tests(tmp_path)


def test_streams_sfst(tmp_path):
    hfst.set_default_fst_type(hfst.ImplementationType.SFST_TYPE)
    run_tests(tmp_path)
