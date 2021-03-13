@ECHO OFF

for %%i in (test_dir_hfst.py test_dir_hfst_exceptions.py ^
    test_dir_hfst_sfst_rules.py ^
    test_tokenizer.py test_exceptions.py test_xre.py ^
    test_read_att_transducer.py test_prolog.py ^
    test_att_reader.py test_prolog_reader.py ^
    test_hfst.py test_examples.py test_pmatch.py test_xerox_rules.py) DO echo testing %%i & %1 >NUL 2>NUL %%i && echo passed

for %%f in (sfst openfst foma) DO echo testing streams with format %%f & %1 test_streams_1.py %%f | %1 test_streams_2.py %%f | %1 test_streams_3.py %%f && echo passed

del foo
del foo_att_prolog
del testfile3.att
del testfile_.att
del tmp

