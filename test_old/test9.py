import libhfst
tr = libhfst.regex('[a::1 a:b::0.3 (b::0)]::0.7;')
tr.push_weights(libhfst.TO_INITIAL_STATE)
print(tr)
tr.push_weights(libhfst.TO_FINAL_STATE)
print(tr)
