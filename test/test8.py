import libhfst
tr = libhfst.read_att_string('0 1 @0@ foo \n\
1 2 ' + libhfst.UNKNOWN + ' ' + libhfst.UNKNOWN + '\n\
2')
print('lookup with output formats tuple, text, raw:')
print(tr.lookup('b', output='tuple'))
print(tr.lookup('b', output='text'))
print(tr.lookup('b', output='raw'))

print(tr.extract_paths(output='dict'))
print(tr.extract_paths(output='text'))
print(tr.extract_paths(output='raw'))
