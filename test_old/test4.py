import libhfst
istr = libhfst.HfstInputStream()
while not istr.is_eof():
    tr = istr.read()
    print('Read transducer:')
    print(tr)
istr.close()
