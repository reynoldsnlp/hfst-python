# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 2:
    sys.path.insert(0, sys.argv[2])
import hfst
if len(sys.argv) < 1:
    raise RuntimeError('Transducer format must be given as first argument')

if sys.argv[1] == 'sfst':
    if not hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.SFST_TYPE):
        sys.exit(77)
    hfst.set_default_fst_type(hfst.ImplementationType.SFST_TYPE)
elif sys.argv[1] == 'foma':
    if not hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.FOMA_TYPE):
        sys.exit(77)
    hfst.set_default_fst_type(hfst.ImplementationType.FOMA_TYPE)
elif sys.argv[1] == 'openfst':
    if not hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.TROPICAL_OPENFST_TYPE):
        sys.exit(77)
    hfst.set_default_fst_type(hfst.ImplementationType.TROPICAL_OPENFST_TYPE)
else:
    raise RuntimeError('implementation format not recognized')

tr1 = hfst.regex('föö:bär')
tr2 = hfst.regex('0')
tr3 = hfst.regex('0-0')
trs = [tr1, tr2, tr3]

ostr = hfst.HfstOutputStream()
ostr.write(trs)
ostr.flush()
ostr.close()
