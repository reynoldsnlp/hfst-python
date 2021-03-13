import pytest

import hfst


@pytest.mark.xfail(reason='This was not being run earlier. May be a faulty test')
def test_2():
    # Create a HFST basic transducer [a:b] with transition weight 0.3 and final weight 0.5.
    t = hfst.HfstBasicTransducer()
    t.add_state(1)
    t.add_transition(0, 1, 'a', 'b', 0.3)
    t.set_final_weight(1, 0.5)

    # Convert to tropical OpenFst format (the default) and push weights toward final state.
    T = hfst.HfstTransducer(t, hfst.get_default_fst_type())
    T.push_weights_to_end()

    # Convert back to HFST basic transducer.
    tc = hfst.HfstBasicTransducer(T)
    try:
        # Rounding might affect the precision.
        assert (0.79 < tc.get_final_weight(1)) and (tc.get_final_weight(1) < 0.81)
    except hfst.exceptions.HfstException:
        assert False, 'The state does not exist or is not final'


def test_3():
    tok = hfst.HfstTokenizer()
    tok.add_multichar_symbol('foo')
    tok.add_multichar_symbol('bar')
    tr = hfst.tokenized_fst(tok.tokenize('foobar', 'foobaz'))
    print(tr)


@pytest.mark.xfail(reason='Need a transducer file to read from.')
def test_4():
    istr = hfst.HfstInputStream()
    while not istr.is_eof():
        tr = istr.read()
        print('Read transducer:')
        print(tr)
    istr.close()


def test_5():
    hfst.set_default_fst_type(hfst.ImplementationType.FOMA_TYPE)
    ab = hfst.regex('a:b')
    out = hfst.HfstOutputStream(hfst_format=False)
    out.write(ab)
    out.flush()
    out.close()


def test_7a():
    fsm = hfst.HfstBasicTransducer()
    fsm.add_state(1)
    fsm.set_final_weight(1, 2.0)
    fsm.add_transition(0, 1, "foo", hfst.EPSILON)
    assert hfst.HfstTransducer(fsm).compare(hfst.regex('foo:0::2.0'))


def test_7b():
    fsm = hfst.HfstBasicTransducer()
    fsm.add_state(1)
    fsm.set_final_weight(1, -0.5)
    fsm.add_transition(0, 1, "foo", hfst.UNKNOWN)
    fsm.add_transition(0, 1, "foo", "foo")
    assert hfst.HfstTransducer(fsm).compare(hfst.regex('foo:?::-0.5'))


def test_7c():
    fsm = hfst.HfstBasicTransducer()
    fsm.add_state(1)
    fsm.set_final_weight(1, 1.5)
    fsm.add_transition(0, 1, hfst.IDENTITY, hfst.IDENTITY)
    assert hfst.HfstTransducer(fsm).compare(hfst.regex('?::1.5'))


def test_8():
    tr = hfst.read_att_string('0 1 @0@ foo \n\
    1 2 ' + hfst.UNKNOWN + ' ' + hfst.UNKNOWN + '\n\
    2')
    print('lookup with output formats tuple, text, raw:')
    print(tr.lookup('b', output='tuple'))
    print(tr.lookup('b', output='text'))
    print(tr.lookup('b', output='raw'))

    print(tr.extract_paths(output='dict'))
    print(tr.extract_paths(output='text'))
    print(tr.extract_paths(output='raw'))


def test_9():
    tr = hfst.regex('[a::1 a:b::0.3 (b::0)]::0.7;')
    tr.push_weights_to_start()
    print(tr)
    tr.push_weights_to_end()
    print(tr)
