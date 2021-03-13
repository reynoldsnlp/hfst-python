# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst

for n in [1, 2, 3]:
    assert(hfst.compile_twolc_file('test'+str(n)+'.twolc', 'test'+str(n)+'.hfst') == 0)

if hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.FOMA_TYPE):
    for n in [1, 2, 3]:
        assert(hfst.compile_twolc_file('test'+str(n)+'.twolc', 'test'+str(n)+'.hfst', verbose=True, type=hfst.ImplementationType.FOMA_TYPE) == 0)
