import libhfst
tok = libhfst.HfstTokenizer()
tok.add_multichar_symbol('foo')
tok.add_multichar_symbol('bar')
tr = libhfst.tokenized_fst(tok.tokenize('foobar', 'foobaz'))
print(tr)
