# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst

types = []
if hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.SFST_TYPE):
    types.append(hfst.ImplementationType.SFST_TYPE)
if hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.TROPICAL_OPENFST_TYPE):
    types.append(hfst.ImplementationType.TROPICAL_OPENFST_TYPE)
if hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.FOMA_TYPE):
    types.append(hfst.ImplementationType.FOMA_TYPE)

from hfst.xerox_rules import *
from hfst import regex

for type in types:
    if hfst.HfstTransducer.is_implementation_type_available(type):

        hfst.set_default_fst_type(type)

        rule = Rule() # just testing the default constructor

        mapping = ( (regex('a'),regex('b')), )
        rule = Rule(mapping)
        assert(replace(rule, False).compare(regex('a -> b')))
        assert(replace(rule, True).compare(regex('a (->) b')))

        mapping = ( (regex('a'),regex('b')), (regex('b'),regex('a')) )
        rule = Rule(mapping)
        assert(replace(rule, False).compare(regex('a -> b, b -> a')))
        assert(replace(rule, True).compare(regex('a (->) b, b (->) a')))

        for repl_type in [(ReplaceType.REPL_UP, '||'), (ReplaceType.REPL_DOWN, '\\/'), (ReplaceType.REPL_LEFT, '\\\\'), (ReplaceType.REPL_RIGHT,'//')]:

            mapping1 = ( (regex('a'),regex('b')), )
            context1 = ( (regex('c'),regex('c')), )

            rule1 = Rule(mapping1, context1, repl_type[0])
            assert(replace(rule1, False).compare(regex('a -> b ' + repl_type[1] + ' c _ c')))
            assert(replace(rule1, True).compare(regex('a (->) b ' + repl_type[1] + ' c _ c')))

            mapping2 = ( (regex('a'),regex('b')), (regex('b'),regex('a')) )
            context2 = ( (regex('c'),regex('c')), (regex('d'),regex('d')) )

            rule2 = Rule(mapping2, context2, repl_type[0])
            assert(replace(rule2, False).compare(regex('a -> b, b -> a ' + repl_type[1] + ' c _ c, d _ d')))
            assert(replace(rule2, True).compare(regex('a (->) b, b (->) a ' + repl_type[1] + ' c _ c, d _ d')))

            rules = (rule1, rule2)
            assert(replace(rules, False).compare(regex('a -> b ' + repl_type[1] + ' c _ c ,, a -> b, b -> a ' + repl_type[1] + ' c _ c, d _ d')))
            assert(replace(rules, True).compare(regex('a (->) b ' + repl_type[1] + ' c _ c ,, a (->) b, b (->) a ' + repl_type[1] + ' c _ c, d _ d')))
