import inspect
import io
import os.path
import sys

import hfst

RSRC_DIR = os.path.dirname(__file__) + '/resources/'


def check_tokenized(tok, pathin, pathout, exp, weight=0):
    tokenized = None
    if pathout is None:
        tokenized = tok.tokenize_one_level(pathin)
    else:
        tokenized = tok.tokenize(pathin, pathout)
    assert hfst.tokenized_fst(tokenized, weight).compare(hfst.regex(exp)), \
        'check_tokenized failed with input: ' + pathin + ", " + pathout


# def get_linenumber():
#     cf = inspect.currentframe()
#     return cf.f_back.f_lineno


# def lookup_fd(self, lookup_path, **kwargs):
#     max_weight = None
#     infinite_cutoff = -1 # Is this right?
#     output='dict' # 'dict' (default), 'text', 'raw'


def unicode(s, c):
    return s


def check_fst(input, result):
    tr1_ = hfst.fst(input)
    tr2_ = hfst.regex(result)
    assert tr1_.compare(tr2_), 'check_fst failed with input: ' + input


def test_hfst(tmp_path):
    types = []
    if hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.TROPICAL_OPENFST_TYPE):
        types.append(hfst.ImplementationType.TROPICAL_OPENFST_TYPE)
    if hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.FOMA_TYPE):
        types.append(hfst.ImplementationType.FOMA_TYPE)

    for type in types:
        print('\n--- Testing implementation type %s ---\n' % hfst.fst_type_to_string(type))

        hfst.set_default_fst_type(type)

        tr1 = None
        tr2 = None
        tr3 = None

        type_ = hfst.ImplementationType.TROPICAL_OPENFST_TYPE
        foobar_path = str(tmp_path / 'foobar.hfst')
        ostr = hfst.HfstOutputStream(filename=foobar_path, type=type_)

        tr_ = hfst.regex('{foo}:{bar}::0.5')
        tr_.convert(type_)

        ostr.write(tr_)
        ostr.write(tr_)
        ostr.flush()
        ostr.close()

        assert os.path.isfile(foobar_path), 'Missing file: ' + foobar_path

        istr = hfst.HfstInputStream(foobar_path)
        numtr = 0
        try:
            tr1 = istr.read()
            numtr += 1
            tr2 = istr.read()
            numtr += 1
            tr3 = istr.read()  # TODO never used
            numtr += 1
        except hfst.exceptions.EndOfStreamException:
            pass
        istr.close()

        assert numtr == 2

        tr1.convert(hfst.get_default_fst_type())
        tr2.convert(hfst.get_default_fst_type())

        foobar2_path = str(tmp_path / 'foobar2.hfst')
        ostr = hfst.HfstOutputStream(filename=foobar2_path)
        ostr.write(tr1)
        ostr.write(tr2)
        ostr.flush()
        ostr.close()

        TR1 = None
        TR2 = None
        TR3 = None

        istr = hfst.HfstInputStream(foobar2_path)
        numtr = 0
        try:
            TR1 = istr.read()
            numtr += 1
            TR2 = istr.read()
            numtr += 1
            TR3 = istr.read()  # TODO never used
            numtr += 1
        except hfst.exceptions.EndOfStreamException:
            pass
        istr.close()

        assert numtr == 2

        assert TR1.compare(tr1)
        assert TR2.compare(tr2)

        # Copy constructor
        transducer = hfst.HfstTransducer(TR1)
        assert TR1.compare(transducer)
        assert transducer.compare(TR1)

        # Read lexc
        tr = hfst.compile_lexc_file(RSRC_DIR + 'test.lexc')
        tr.insert_freely(tr1)
        tr.minimize()
        tr.insert_freely(('A', 'B'))
        tr.minimize()

        # Read sfst
        tr = hfst.compile_sfst_file(RSRC_DIR + 'test.sfstpl')
        assert tr is not None

        # Substitute
        tr = hfst.regex('a a:b b;')
        tr.substitute('a', 'A', input=True, output=False)
        eq = hfst.regex('A:a A:b b;')
        assert tr.compare(eq)

        tr = hfst.regex('a a:b b;')
        tr.substitute('a', 'A', input=False, output=True)
        eq = hfst.regex('a:A a:b b;')
        assert tr.compare(eq)

        tr = hfst.regex('a a:b b;')
        tr.substitute('a', 'A')
        eq = hfst.regex('A A:b b;')
        assert tr.compare(eq)

        tr = hfst.regex('a a:b b;')
        tr.substitute(('a', 'b'), ('A', 'B'))
        eq = hfst.regex('a A:B b;')
        assert tr.compare(eq)

        tr = hfst.regex('a a:b b;')
        tr.substitute(('a', 'b'), (('A', 'B'), ('B', 'C'), ('C', 'D')))
        eq = hfst.regex('a [A:B|B:C|C:D] b;')
        assert tr.compare(eq)

        tr = hfst.regex('a a:b b;')
        tr.substitute(('a', 'b'), (('A', 'B'), ('B', 'C'), ('C', 'D')))
        eq = hfst.regex('a [A:B|B:C|C:D] b;')
        assert tr.compare(eq)

        tr = hfst.regex('a a:b b;')
        tr.substitute({'a': 'A', 'b': 'B', 'c': 'C'})
        eq = hfst.regex('A A:B B;')
        assert tr.compare(eq)

        tr = hfst.regex('a a:b b;')
        tr.substitute({('a', 'a'): ('A', 'a'), ('a', 'b'): ('a', 'B'), ('c', 'c'): ('C', 'c')})
        eq = hfst.regex('A:a a:B b;')
        assert tr.compare(eq)

        tr = hfst.regex('a a:b b;')
        sub = hfst.regex('[c:d]+;')
        tr.substitute(('a', 'b'), sub)
        eq = hfst.regex('a [c:d]+ b;')
        assert tr.compare(eq)

        # push weights
        tr = hfst.regex('[a::1 a:b::0.3 b::0]::0.7;')
        tr.push_weights_to_start()
        tr.push_weights_to_end()

        # set final weights
        tr = hfst.regex('(a a:b (b));')
        tr.set_final_weights(0.1)
        tr.set_final_weights(0.4, True)

        # reading and writing in text format
        f = open(tmp_path / 'testfile_.att', 'w')
        f.write('\n'.join(['0 1 foo bar 0.5',
                           '0 1 fo ba 0.2',
                           '0 1 f b 0',
                           '1 2 baz baz',
                           '2 0.1',
                           '--\n\n']))
        f.close()

        numtr = 0
        f = open(tmp_path / 'testfile_.att', 'r')
        try:
            while True:
                TR = hfst.read_att_transducer(f)
                numtr += 1
        except hfst.exceptions.EndOfStreamException:
            pass
        f.close()
        assert numtr == 2

        f = open(tmp_path / 'foo_att_prolog', 'w')
        f.write('-- in ATT format --\n')
        TR.write_att(f)
        f.write('-- in prolog format --\n')
        TR.write_prolog(f)
        f.close()

        fsm = hfst.read_att_string('''0\t 1 a b
                                      1 2 c   d 0.5
                                      2
                                      2 3 \t\te f
                                      3   0.3 ''')
        # assert fsm.compare(hfst.regex('a:b c:d::0.5 (e:f::0.3)'), 'read_att_string failed'

        # Lookup and path extraction
        tr = hfst.regex('foo:bar::0.5 | foo:baz')

        f = open(tmp_path / 'foo', 'w')
        try:
            print(tr.lookup('foo', max_number=5, output='text'), file=f)
        except hfst.exceptions.FunctionNotImplementedException:
            TR = hfst.HfstTransducer(tr)
            TR.convert(hfst.ImplementationType.HFST_OLW_TYPE)
            print(TR.lookup('foo', max_number=5, output='text'), file=f)

        tr_ = tr.copy()
        tr.lookup_optimize()
        tr.lookup('foo', max_number=5, output='text', file=f)
        tr.remove_optimization()
        assert tr.compare(tr_)

        fsm = hfst.HfstBasicTransducer(tr)
        print(fsm.lookup((('foo'))), file=f)

        print(tr.extract_paths(obey_flags='True', filter_flags='False', max_number=3, output='dict'), file=f)

        f.close()

        # Create automaton:
        # unweighted
        check_fst('foobar', '[f o o b a r]')
        check_fst(['foobar'], '[f o o b a r]')
        check_fst(['foobar', 'foobaz'], '[f o o b a [r|z]]')
        # with weights
        check_fst(('foobar', 0.3), '[f o o b a r]::0.3')
        check_fst([('foobar', 0.5)], '[f o o b a r]::0.5')
        check_fst(['foobar', ('foobaz', -2)], '[ f o o b a [r|[z::-2]] ]')
        # Special inputs
        check_fst('*** FOO ***', '{*** FOO ***}')

        foo = hfst.fst('')
        eps = hfst.epsilon_fst()
        assert foo.compare(eps)
        # try:
        #     foo = hfst.fst('')
        #     raise RuntimeError(get_linenumber())
        # except RuntimeError as e:
        #     if not e.__str__() == 'Empty word.':
        #         raise RuntimeError(get_linenumber())

        # Create transducer:
        # unweighted
        check_fst({'foobar': 'foobaz'}, '[f o o b a r:z]')
        check_fst({'foobar': ['foobar', 'foobaz']}, '[f o o b a [r|r:z]]')
        check_fst({'foobar': ('foobar', 'foobaz')}, '[f o o b a [r|r:z]]')
        check_fst({'foobar': 'foobaz', 'FOOBAR': ('foobar', 'FOOBAR'), 'Foobar': ['Foo', 'bar', 'Foobar']}, '[f o o b a r:z] | [F O O B A R] | [F:f O:o O:o B:b A:a R:r] | [F o o b:0 a:0 r:0] | [F:b o:a o:r b:0 a:0 r:0] | [F o o b a r]')

        # with weights
        check_fst({'foobar': ('foobaz', -1)}, '[f o o b a r:z]::-1')
        check_fst({'foobar': ['foobar', ('foobaz', -2.0)]}, '[f o o b a [r|r:z::-2.0]]')
        check_fst({'foobar': ('foobar', ('foobaz', 3.5))}, '[f o o b a [r|r:z::3.5]]')
        check_fst({'foobar': ('foobaz', -1), 'FOOBAR': ('foobar', ('FOOBAR', 2)), 'Foobar': [('Foo', 2.5), 'bar', ('Foobar', 0.3)]}, '[f o o b a r:z]::-1 | [F O O B A R]::2 | [F:f O:o O:o B:b A:a R:r] | [F o o b:0 a:0 r:0]::2.5 | [F:b o:a o:r b:0 a:0 r:0] | [F o o b a r]::0.3')

        # Special inputs
        check_fst({'*** FOO ***': '+++ BAR +++'}, '{*** FOO ***}:{+++ BAR +++}')

        foo = hfst.fst({'': 'foo'})
        tr = hfst.regex('0:{foo}')
        assert foo.compare(tr)
        foo = hfst.fst({'foo': ''})
        tr = hfst.regex('{foo}:0')
        assert foo.compare(tr)
        # try:
        #     foo = hfst.fst({'':'foo'})
        #     raise RuntimeError(get_linenumber())
        # except RuntimeError as e:
        #     if not e.__str__() == 'Empty word.':
        #         raise RuntimeError(get_linenumber())
        # try:
        #     foo = hfst.fst({'foo':''})
        #     raise RuntimeError(get_linenumber())
        # except RuntimeError as e:
        #     if not e.__str__() == 'Empty word.':
        #         raise RuntimeError(get_linenumber())

        # Tokenized input
        tok = hfst.HfstTokenizer()

        check_tokenized(tok, 'foobar', None, '[f o o b a r]')
        check_tokenized(tok, 'foobar', 'foobar', '[f o o b a r]')
        check_tokenized(tok, 'foobar', 'foobaz', '[f o o b a r:z]')
        check_tokenized(tok, 'fööbär?', None, '[f ö ö b ä r "?"]')
        check_tokenized(tok, 'fööbär?', 'fööbär?', '[f ö ö b ä r "?"]')
        check_tokenized(tok, 'fööbär?', 'fööbäz!', '[f ö ö b ä r:z "?":"!"]::0.5', 0.5)

        check_tokenized(tok, 'foo', None, '[f o o]')
        check_tokenized(tok, 'foobar', 'foo', '[f o o b:0 a:0 r:0]')
        check_tokenized(tok, 'bar', 'foobaz', '[b:f a:o r:o 0:b 0:a 0:z]')
        check_tokenized(tok, 'bär?', None, '[b ä r "?"]')
        check_tokenized(tok, 'fööbär?', 'bär?', '[f:b ö:ä ö:r b:"?" ä:0 r:0 "?":0]')
        check_tokenized(tok, 'bär?', 'fööbäz!', '[b:f ä:ö r:ö "?":b 0:ä 0:z 0:"!"]')

        tok.add_skip_symbol('fö')
        tok.add_multichar_symbol('föö')
        tok.add_multichar_symbol('fööbär')

        check_tokenized(tok, 'föbär', None, '[b ä r]')
        check_tokenized(tok, 'fööbär', None, '[fööbär]')
        check_tokenized(tok, 'föfööfö', None, '[föö]')

        check_tokenized(tok, 'föbär', 'foofö', '[b:f ä:o r:o]')
        check_tokenized(tok, 'fööbär', 'föbar', '[fööbär:b 0:a 0:r]')
        check_tokenized(tok, 'föfööfö', 'föföföföö', '[föö]')

        tok = hfst.HfstTokenizer()
        tok.add_skip_symbol('?')
        tok.add_skip_symbol(' ')
        check_tokenized(tok, 'How is this tokenized?', None, '[H o w i s t h i s t o k e n i z e d]')
        tok.add_skip_symbol(' is ')
        check_tokenized(tok, 'How is this tokenized?', None, '[H o w t h i s t o k e n i z e d]')

        tok = hfst.HfstTokenizer()
        tok.add_multichar_symbol(hfst.EPSILON)  # TODO should this be included by default???
        check_tokenized(tok, '@_EPSILON_SYMBOL_@foo', None, '[f o o]')

        assert hfst.tokenized_fst([(hfst.EPSILON, 'b'), ('f', 'a'), ('o', 'a'), ('o', 'r')]).compare(hfst.regex('[0:b f:a o:a o:r]'))

        # Is this ok???
        assert hfst.regex('"' + hfst.EPSILON + '"').compare(hfst.regex('[0]'))
        assert hfst.regex('"' + hfst.IDENTITY + '"').compare(hfst.regex('[?]'))
        assert hfst.regex('"' + hfst.UNKNOWN + '":"' + hfst.UNKNOWN + '"').compare(hfst.regex('[?:?]'))

        # other python functions
        assert hfst.empty_fst().compare(hfst.regex('[0-0]'))
        assert hfst.epsilon_fst().compare(hfst.regex('[0]'))
        assert hfst.epsilon_fst(-1.5).compare(hfst.regex('[0]::-1.5'))

        # Non-ascii characters and unknowns/identities
        tr1 = hfst.regex('Ä:é å ?;')
        tr2 = hfst.regex('? Ö;')
        tr1.concatenate(tr2)
        result = hfst.regex('Ä:é å [Ä|é|å|Ö|?] [Ä|é|å|Ö|?] Ö;')
        assert tr1.compare(result)

        tr1 = hfst.regex('ñ ?:á;')
        tr2 = hfst.regex('Ê:?;')
        tr1.concatenate(tr2)
        result = hfst.regex('ñ [ñ:á|á|Ê:á|?:á] [Ê:ñ|Ê|Ê:á|Ê:?];')
        assert tr1.compare(result)

        # Other functions (TODO: more extensixe checks)
        tr = hfst.regex('[foo]|[foo bar]|[f o o bar baz]')
        assert tr.longest_path_size() == 5
        result = tr.extract_longest_paths()
        assert len(result) == 1
        result = tr.extract_shortest_paths()
        assert len(result) == 1

        # XfstCompiler
        if int(sys.version[0]) > 2:
            msg = io.StringIO()
            assert hfst.compile_xfst_file(RSRC_DIR + 'test_pass.xfst', verbosity=0, output=msg, error=msg) == 0
            assert hfst.compile_xfst_file(RSRC_DIR + 'test_fail.xfst', verbosity=0, output=msg, error=msg) != 0
            assert hfst.compile_xfst_file(RSRC_DIR + 'test_fail.xfst', quit_on_fail=False, verbosity=0, output=msg, error=msg) == 0

        # regex compiler
        msg = io.StringIO()
        msg.write(unicode('This is the error message:\n', 'utf-8'))
        tr = hfst.regex('foo\\', error=msg)
        if tr is None:
            msg.write(unicode('This was the error message.\n', 'utf-8'))
            # print(msg.getvalue())
        msg = sys.stdout
        tr = hfst.regex('foo\\', error=msg)

        # lexc compiler
        msg = io.StringIO()
        tr = hfst.compile_lexc_file(RSRC_DIR + 'test.lexc', output=msg, verbosity=2)
        # print('This is the output from lexc:')
        # print(msg.getvalue())

        # default constructor
        tr = hfst.HfstTransducer()
        assert tr.compare(hfst.empty_fst())

        defs = {'foo': hfst.regex('Foo'), 'bar': hfst.regex('Bar')}
        tr = hfst.regex('foo bar', definitions=defs)
        assert tr.compare(hfst.regex('Foo Bar'))
        tr = hfst.regex('foo bar')
        assert tr.compare(hfst.regex('foo bar'))

    # print('\n--- Testing HfstBasicTransducer ---\n')

    # Create basic transducer, write it to file, read it, and test equivalence
    fsm = hfst.HfstBasicTransducer()
    fsm.add_state(0)
    fsm.add_state(1)
    fsm.set_final_weight(1, 0.3)
    tr = hfst.HfstBasicTransition(1, 'foo', 'bar', 0.5)
    fsm.add_transition(0, tr)
    fsm.add_transition(0, 0, 'baz', 'baz')
    fsm.add_transition(0, 0, 'baz', 'BAZ', 0.1)

    f = open(tmp_path / 'foo_basic', 'w')
    fsm.write_att(f)
    f.close()

    f = open(tmp_path / 'foo_basic', 'r')
    fsm2 = hfst.HfstBasicTransducer(hfst.read_att_transducer(f, hfst.EPSILON))  # TODO never used
    f.close()

    # Modify weights of a basic transducer
    fsm = hfst.HfstBasicTransducer()
    fsm.add_state(0)
    fsm.add_state(1)
    fsm.set_final_weight(1, 0.3)
    fsm.add_transition(0, 0, 'baz', 'baz')
    arcs = fsm.transitions(0)
    arcs[0].set_weight(0.5)
    arcs = fsm.transitions(0)
    assert arcs[0].get_weight() == 0.5

    # comparison can fail because of rounding
    # for type in types:
    #     FSM = hfst.HfstTransducer(fsm, type)
    #     FSM2 = hfst.HfstTransducer(fsm2, type)
    #
    #     assert FSM.compare(FSM2)
    #
    # this test does not assert anything
    # for type in types:
    #     FSM.convert(type)
    #     Fsm = hfst.HfstBasicTransducer(FSM)
    #     FSM2.convert(type)
    #     Fsm2 = hfst.HfstBasicTransducer(FSM2)

    # Print basic transducer
    fsm = hfst.HfstBasicTransducer()
    for state in [0, 1, 2]:
        fsm.add_state(state)
    fsm.add_transition(0, 1, 'foo', 'bar', 1)
    fsm.add_transition(0, 1, 'foo', 'BAR', 2)
    fsm.add_transition(1, 2, 'baz', 'baz', 0)
    fsm.set_final_weight(2, 0.5)

    # Different ways to print the transducer
    f = open(tmp_path / 'foo', 'w')
    for state in fsm.states():
        for arc in fsm.transitions(state):
            print('%i ' % (state), end='', file=f)
            print(arc, file=f)
        if fsm.is_final_state(state):
            print('%i %f' % (state, fsm.get_final_weight(state)), file=f)

    for state, arcs in enumerate(fsm):
        for arc in arcs:
            print('%i ' % (state), end='', file=f)
            print(arc, file=f)
        if fsm.is_final_state(state):
            print('%i %f' % (state, fsm.get_final_weight(state)), file=f)

    index = 0
    for state in fsm.states_and_transitions():
        for transition in state:
            print('%u\t%u\t%s\t%s\t%.2f' % (index, transition.get_target_state(), transition.get_input_symbol(), transition.get_output_symbol(), transition.get_weight()), file=f)
        if fsm.is_final_state(index):
            print('%s\t%.2f' % (index, fsm.get_final_weight(index)), file=f)
        index = index + 1

    print(fsm, file=f)
    f.close()

    tr = hfst.HfstBasicTransducer(hfst.regex('foo'))
    tr.substitute({'foo': 'bar'})
    tr.substitute({('foo', 'foo'): ('bar', 'bar')})

    tr = hfst.fst({'foo': 'bar'})
    fst = hfst.HfstBasicTransducer(tr)
    fsa = hfst.fst_to_fsa(fst, '^')
    fst = hfst.fsa_to_fst(fsa, '^')
    TR = hfst.HfstTransducer(fst)
    assert TR.compare(tr)

    tr = hfst.regex('{foo}:{bar}|{FOO}:{BAR}')
    fsm = hfst.HfstBasicTransducer(tr)
    net = fsm.states_and_transitions()
    for state in net:
        for arc in state:
            arc.set_input_symbol(arc.get_input_symbol() + '>')
            arc.set_output_symbol('<' + arc.get_output_symbol())
            arc.set_weight(arc.get_weight() - 0.5)

    for state, arcs in enumerate(fsm):
        for arc in arcs:
            arc.set_input_symbol('<' + arc.get_input_symbol())
            arc.set_output_symbol(arc.get_output_symbol() + '>')
            arc.set_weight(arc.get_weight() - 1.5)

    for state in fsm:
        for arc in state:
            arc.set_input_symbol('' + arc.get_input_symbol() + '')
            arc.set_output_symbol('' + arc.get_output_symbol() + '')
            arc.set_weight(arc.get_weight() - 0.5)

    tr = hfst.regex('[["<f>" "<o>" "<o>"]:["<b>" "<a>" "<r>"]|["<F>" "<O>" "<O>"]:["<B>" "<A>" "<R>"]]::-7.5')
    assert tr is not None
    TR = hfst.HfstTransducer(fsm)
    assert TR.compare(tr)
