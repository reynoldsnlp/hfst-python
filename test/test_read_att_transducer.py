import os.path

import hfst

RSRC_DIR = os.path.dirname(__file__) + '/resources/'


def test_read_att_transducer():
    for type in [hfst.ImplementationType.SFST_TYPE,
                 hfst.ImplementationType.TROPICAL_OPENFST_TYPE,
                 hfst.ImplementationType.FOMA_TYPE]:
        if hfst.HfstTransducer.is_implementation_type_available(type):

            transducers = []
            ifile = open(RSRC_DIR + 'testfile.att', 'r')
            try:
                while (True):
                    t = hfst.read_att_transducer(ifile, '<eps>')
                    transducers.append(t)
            except hfst.exceptions.NotValidAttFormatException:
                print("Error reading transducer: not valid AT&T format.")
            except hfst.exceptions.EndOfStreamException:
                pass
            ifile.close()
            assert len(transducers) == 4
