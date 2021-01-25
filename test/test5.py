import libhfst
libhfst.set_default_fst_type(libhfst.FOMA_TYPE)
ab = libhfst.regex('a:b')
out = libhfst.HfstOutputStream(hfst_format=False)
out.write(ab)
out.flush()
out.close()
