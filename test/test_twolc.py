import os.path

import hfst

RSRC_DIR = os.path.dirname(__file__) + '/resources/'


def test_twolc(tmp_path):
    for n in [1, 2, 3]:
        assert hfst.compile_twolc_file(RSRC_DIR + 'test' + str(n) + '.twolc', str(tmp_path / 'twolc_test') + str(n) + '.hfst') == 0

    if hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.FOMA_TYPE):
        for n in [1, 2, 3]:
            assert hfst.compile_twolc_file(RSRC_DIR + 'test' + str(n) + '.twolc', str(tmp_path / 'twolc_foma_test') + str(n) + '.hfst', verbose=True, type=hfst.ImplementationType.FOMA_TYPE) == 0
