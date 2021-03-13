# -*- coding: utf-8 -*-
import sys
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])
import hfst.sfst_rules

diritems = \
['coercion', 'deep_coercion', 'deep_restriction', 'deep_restriction_and_coercion', \
 'left_replace_down', 'left_replace_down_karttunen', 'left_replace_left', 'left_replace_right', \
 'left_replace_up', 'replace_down', 'replace_down_karttunen', 'replace_left', 'replace_right', \
 'replace_up', 'restriction', 'restriction_and_coercion', 'surface_coercion', 'surface_restriction', \
 'surface_restriction_and_coercion', 'two_level_if', 'two_level_if_and_only_if', 'two_level_only_if']

dirhfstsfstrules = dir(hfst.sfst_rules)

for item in diritems:
    assert item in dirhfstsfstrules
