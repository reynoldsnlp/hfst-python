# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst

diritems = \
['EPSILON',
 'HfstBasicTransducer', 'HfstBasicTransition', 'HfstInputStream', 'HfstOutputStream',
 'HfstTokenizer', 'HfstTransducer', 'IDENTITY', 'LexcCompiler', 'PmatchContainer',
 'UNKNOWN',
 'XfstCompiler', 'XreCompiler', 'compile_lexc_file',
 'compile_pmatch_expression', 'compile_pmatch_file', 'compile_xfst_file', 'concatenate', 'disjunct',
 'empty_fst', 'epsilon_fst', 'exceptions', 'fsa', 'fst', 'fst_type_to_string', 'get_default_fst_type',
 'get_output_to_console', 'intersect', 'is_diacritic',
 'read_att_input', 'read_att_string', 'regex', 'sfst_rules', 'xerox_rules', 'set_default_fst_type',
 'set_output_to_console', 'start_xfst', 'tokenized_fst']

dirhfst = dir(hfst)

for item in diritems:
    if not item in dirhfst:
        print('error: dir(hfst) does not contain', item)
        assert(False)

assert hfst.EPSILON == '@_EPSILON_SYMBOL_@'
assert hfst.UNKNOWN == '@_UNKNOWN_SYMBOL_@'
assert hfst.IDENTITY == '@_IDENTITY_SYMBOL_@'

assert hfst.ImplementationType.SFST_TYPE == 0
assert hfst.ImplementationType.TROPICAL_OPENFST_TYPE == 1
assert hfst.ImplementationType.LOG_OPENFST_TYPE == 2
assert hfst.ImplementationType.FOMA_TYPE == 3
assert hfst.ImplementationType.XFSM_TYPE == 4
assert hfst.ImplementationType.HFST_OL_TYPE == 5
assert hfst.ImplementationType.HFST_OLW_TYPE == 6
assert hfst.ImplementationType.HFST2_TYPE == 7
assert hfst.ImplementationType.UNSPECIFIED_TYPE == 8
assert hfst.ImplementationType.ERROR_TYPE == 9
