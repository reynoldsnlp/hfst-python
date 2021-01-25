# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst

import os.path
assert os.path.isfile('streets.txt')

# pmatch transducers are always in ol format, so this has actually no effect...
for type in [hfst.ImplementationType.SFST_TYPE, hfst.ImplementationType.TROPICAL_OPENFST_TYPE, hfst.ImplementationType.FOMA_TYPE]:
    if hfst.HfstTransducer.is_implementation_type_available(type):
        hfst.set_default_fst_type(type)

        # (1) compile the file directly
        defs = hfst.compile_pmatch_file('streets.txt')
        cont = hfst.PmatchContainer(defs)
        assert cont.match("Je marche seul dans l'avenue des Ternes.") == "Je marche seul dans l'<FrenchStreetName>avenue des Ternes</FrenchStreetName>."

        # (2) compile the contents of file
        with open('streets.txt', 'r') as myfile:
            data=myfile.read()
            myfile.close()
        defs = hfst.compile_pmatch_expression(data)
        cont = hfst.PmatchContainer(defs)
        assert cont.match("Je marche seul dans l'avenue des Ternes.") == "Je marche seul dans l'<FrenchStreetName>avenue des Ternes</FrenchStreetName>."
        
        # (3) try to compile a nonexistent file
        nonexistent_file = 'foofoofoofoofoofoofoofoofoofoofoofoo'
        assert not os.path.isfile(nonexistent_file)
        try:
            hfst.compile_pmatch_file(nonexistent_file)
            assert False
        except IOError as e:
            pass

        # (5) use PmatchContainer.locate
        locations = cont.locate("Je marche seul dans l'avenue des Ternes.")
        assert len(locations) == 3
        assert locations[0][0].input == "Je marche seul dans l'"
        assert locations[0][0].output == "@_NONMATCHING_@"
        assert locations[1][0].input == "avenue des Ternes"
        assert locations[1][0].output == "avenue des Ternes"
        assert locations[2][0].input == "."
        assert locations[2][0].output == "@_NONMATCHING_@"

        # (6) use PmatchContainer.tokenize
        tokenization = cont.get_tokenized_output("Je marche seul dans l'avenue des Ternes.")
        assert tokenization.rstrip() == "avenue des Ternes"
        tokenization = cont.tokenize("Je marche seul dans l'avenue des Ternes.")
        assert tokenization == ["avenue des Ternes"]

        # (7) Test Finnish tokenizer
        if os.path.isfile('finnish-tokenizer.hfstol'):
            #istr = hfst.HfstInputStream('finnish-tokenizer.hfstol')
            #defs = istr.read_all()
            #istr.close()
            #cont = hfst.PmatchContainer(defs)
            cont = hfst.PmatchContainer('finnish-tokenizer.hfstol')
            locations = cont.locate("Tässä on sanoja!")
            assert len(locations) == 6
            assert locations[0][0].input == "Tässä"
            assert locations[1][0].input == " "
            assert locations[2][0].input == "on"
            assert locations[3][0].input == " "
            assert locations[4][0].input == "sanoja"
            assert locations[5][0].input == "!"

            assert cont.match("Tässä on sanoja!") == "tämä Pron Dem Ine Sg olla V Prs Act Sg3 sana N Par Pl!"

            tokenization = cont.get_tokenized_output("Tässä on sanoja!")
            assert tokenization.rstrip() == "Tässä\non\nsanoja\n!"

            # stress test (tested also with 100 000)
            for i in range(10000):
                tokenization = cont.tokenize("Tässä on sanoja!")
            assert tokenization == ["Tässä", "on", "sanoja", "!"]

        # (8) try to compile meaningless and invalid expressions
        # skip these tests, it seems that PmatchCompiler should be reseted after
        # compilation that fails...
        continue
        for expr in ["foobarbaz; ????", "", "efine CapWord UppercaseAlpha Alpha* :"]:
            print(expr)
            try:
                defs = hfst.compile_pmatch_expression(expr)
                assert False
            except hfst.exceptions.HfstException as e:
                pass
