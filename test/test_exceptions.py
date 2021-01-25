# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst.exceptions

# HfstException and its subclasses

e = hfst.exceptions.HfstException()
e = hfst.exceptions.HfstException('foo','bar', 10)
e = hfst.exceptions.HfstTransducerTypeMismatchException('foo','bar', 10)
e = hfst.exceptions.ImplementationTypeNotAvailableException('foo','bar', 10, 1)
e = hfst.exceptions.FunctionNotImplementedException('foo','bar', 10)
e = hfst.exceptions.StreamNotReadableException('foo','bar', 10)
e = hfst.exceptions.StreamCannotBeWrittenException('foo','bar', 10)
e = hfst.exceptions.StreamIsClosedException('foo','bar', 10)
e = hfst.exceptions.EndOfStreamException('foo','bar', 10)
e = hfst.exceptions.TransducerIsCyclicException('foo','bar', 10)
e = hfst.exceptions.NotTransducerStreamException('foo','bar', 10)
e = hfst.exceptions.NotValidAttFormatException('foo','bar', 10)
e = hfst.exceptions.NotValidPrologFormatException('foo','bar', 10)
e = hfst.exceptions.NotValidLexcFormatException('foo','bar', 10)
e = hfst.exceptions.StateIsNotFinalException('foo','bar', 10)
e = hfst.exceptions.ContextTransducersAreNotAutomataException('foo','bar', 10)
e = hfst.exceptions.TransducersAreNotAutomataException('foo','bar', 10)
e = hfst.exceptions.StateIndexOutOfBoundsException('foo','bar', 10)
e = hfst.exceptions.TransducerHeaderException('foo','bar', 10)
e = hfst.exceptions.MissingOpenFstInputSymbolTableException('foo','bar', 10)
e = hfst.exceptions.TransducerTypeMismatchException('foo','bar', 10)
e = hfst.exceptions.EmptySetOfContextsException('foo','bar', 10)
e = hfst.exceptions.SpecifiedTypeRequiredException('foo','bar', 10)
e = hfst.exceptions.HfstFatalException('foo','bar', 10)
e = hfst.exceptions.TransducerHasWrongTypeException('foo','bar', 10)
e = hfst.exceptions.IncorrectUtf8CodingException('foo','bar', 10)
e = hfst.exceptions.EmptyStringException('foo','bar', 10)
e = hfst.exceptions.SymbolNotFoundException('foo','bar', 10)
e = hfst.exceptions.MetadataException('foo','bar', 10)
e = hfst.exceptions.FlagDiacriticsAreNotIdentitiesException('foo','bar', 10)

import hfst

# Test that importing exceptions via a package works
if hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.FOMA_TYPE) and hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.TROPICAL_OPENFST_TYPE):
    try:
        foo = hfst.regex('foo')
        bar = hfst.regex('bar')
        foo.convert(hfst.ImplementationType.FOMA_TYPE)
        bar.convert(hfst.ImplementationType.TROPICAL_OPENFST_TYPE)
        foo.concatenate(bar)
        assert False
    except hfst.exceptions.TransducerTypeMismatchException as e:
        pass

