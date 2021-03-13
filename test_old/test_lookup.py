# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst

for type in [hfst.ImplementationType.SFST_TYPE, hfst.ImplementationType.TROPICAL_OPENFST_TYPE, hfst.ImplementationType.FOMA_TYPE]:
    if hfst.HfstTransducer.is_implementation_type_available(type):
        
        hfst.set_default_fst_type(type)
        tr = hfst.regex('[foo:bar] | [?:B ?:A ?:R]')
        result = tr.lookup('foo')
        assert(len(result) == 1)
        assert(result[0][0] == 'bar')
        tr = hfst.regex('[f:0 o:0 o:foo]')
        result = tr.lookup('foo')
        assert(len(result) == 1)
        assert(result[0][0] == '@_EPSILON_SYMBOL_@@_EPSILON_SYMBOL_@foo')
        tr = hfst.regex('[foo:bar]|[f:B o:A o:R]')
        result = tr.lookup('foo')
        assert(len(result) == 1)
        assert(result[0][0] == 'bar')
