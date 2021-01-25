# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst

for type in [hfst.ImplementationType.SFST_TYPE, hfst.ImplementationType.TROPICAL_OPENFST_TYPE, hfst.ImplementationType.FOMA_TYPE]:
    if hfst.HfstTransducer.is_implementation_type_available(type):

        transducers = []
        ifile = open('testfile.att', 'r')
        try:
            while (True):
                t = hfst.read_att_transducer(ifile, '<eps>')
                transducers.append(t)
        except hfst.exceptions.NotValidAttFormatException as e:
            print("Error reading transducer: not valid AT&T format.")
        except hfst.exceptions.EndOfStreamException as e:
            pass
        ifile.close()
        assert(len(transducers) == 4)

