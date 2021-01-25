import libhfst
# Create a HFST basic transducer [a:b] with transition weight 0.3 and final weight 0.5.
t = libhfst.HfstBasicTransducer()
t.add_state(1)
t.add_transition(0, 1, 'a', 'b', 0.3)
t.set_final_weight(1, 0.5)
#
# Convert to tropical OpenFst format (the default) and push weights toward final state.
T = libhfst.HfstTransducer(t, libhfst.get_default_fst_type())
T.push_weights(libhfst.TO_FINAL_STATE)
#
# Convert back to HFST basic transducer.
tc = libhfst.HfstBasicTransducer(T)
try:
    # Rounding might affect the precision.
    if (0.79 < tc.get_final_weight(1)) and (tc.get_final_weight(1) < 0.81):
        print("TEST PASSED")
        exit(0)
    else:
        print("TEST FAILED")
        exit(1)
# If the state does not exist or is not final */
except libhfst.HfstException:
    print("TEST FAILED: An exception thrown.")
    exit(1)
