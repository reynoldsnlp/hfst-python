import hfst
import hfst.exceptions


def test_exceptions():
    hfst.exceptions.HfstException()
    hfst.exceptions.HfstException('foo', 'bar', 10)
    hfst.exceptions.HfstTransducerTypeMismatchException('foo', 'bar', 10)
    hfst.exceptions.ImplementationTypeNotAvailableException('foo', 'bar', 10, 1)
    hfst.exceptions.FunctionNotImplementedException('foo', 'bar', 10)
    hfst.exceptions.StreamNotReadableException('foo', 'bar', 10)
    hfst.exceptions.StreamCannotBeWrittenException('foo', 'bar', 10)
    hfst.exceptions.StreamIsClosedException('foo', 'bar', 10)
    hfst.exceptions.EndOfStreamException('foo', 'bar', 10)
    hfst.exceptions.TransducerIsCyclicException('foo', 'bar', 10)
    hfst.exceptions.NotTransducerStreamException('foo', 'bar', 10)
    hfst.exceptions.NotValidAttFormatException('foo', 'bar', 10)
    hfst.exceptions.NotValidPrologFormatException('foo', 'bar', 10)
    hfst.exceptions.NotValidLexcFormatException('foo', 'bar', 10)
    hfst.exceptions.StateIsNotFinalException('foo', 'bar', 10)
    hfst.exceptions.ContextTransducersAreNotAutomataException('foo', 'bar', 10)
    hfst.exceptions.TransducersAreNotAutomataException('foo', 'bar', 10)
    hfst.exceptions.StateIndexOutOfBoundsException('foo', 'bar', 10)
    hfst.exceptions.TransducerHeaderException('foo', 'bar', 10)
    hfst.exceptions.MissingOpenFstInputSymbolTableException('foo', 'bar', 10)
    hfst.exceptions.TransducerTypeMismatchException('foo', 'bar', 10)
    hfst.exceptions.EmptySetOfContextsException('foo', 'bar', 10)
    hfst.exceptions.SpecifiedTypeRequiredException('foo', 'bar', 10)
    hfst.exceptions.HfstFatalException('foo', 'bar', 10)
    hfst.exceptions.TransducerHasWrongTypeException('foo', 'bar', 10)
    hfst.exceptions.IncorrectUtf8CodingException('foo', 'bar', 10)
    hfst.exceptions.EmptyStringException('foo', 'bar', 10)
    hfst.exceptions.SymbolNotFoundException('foo', 'bar', 10)
    hfst.exceptions.MetadataException('foo', 'bar', 10)
    hfst.exceptions.FlagDiacriticsAreNotIdentitiesException('foo', 'bar', 10)


    # Test that importing exceptions via a package works
    if hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.FOMA_TYPE) and hfst.HfstTransducer.is_implementation_type_available(hfst.ImplementationType.TROPICAL_OPENFST_TYPE):
        try:
            foo = hfst.regex('foo')
            bar = hfst.regex('bar')
            foo.convert(hfst.ImplementationType.FOMA_TYPE)
            bar.convert(hfst.ImplementationType.TROPICAL_OPENFST_TYPE)
            foo.concatenate(bar)
            assert False
        except hfst.exceptions.TransducerTypeMismatchException:
            pass
