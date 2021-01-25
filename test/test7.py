import libhfst

fsm = libhfst.HfstBasicTransducer()
fsm.add_state(1)
fsm.set_final_weight(1, 2.0)
fsm.add_transition(0, 1, "foo", libhfst.EPSILON)
if not libhfst.HfstTransducer(fsm).compare(libhfst.regex('foo:0::2.0')):
    raise RuntimeError('')
    
fsm = libhfst.HfstBasicTransducer()
fsm.add_state(1)
fsm.set_final_weight(1, -0.5)
fsm.add_transition(0, 1, "foo", libhfst.UNKNOWN)
fsm.add_transition(0, 1, "foo", "foo")
if not libhfst.HfstTransducer(fsm).compare(libhfst.regex('foo:?::-0.5')):
    raise RuntimeError('')

fsm = libhfst.HfstBasicTransducer()
fsm.add_state(1)
fsm.set_final_weight(1, 1.5)
fsm.add_transition(0, 1, libhfst.IDENTITY, libhfst.IDENTITY)
if not libhfst.HfstTransducer(fsm).compare(libhfst.regex('?::1.5')):
    raise RuntimeError('')
