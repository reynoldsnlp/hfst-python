"""

Hfst Xerox-type rule functions and classes.

"""

import hfst.libhfst
from hfst.libhfst import after
from hfst.libhfst import before
from hfst.libhfst import replace
from hfst.libhfst import replace_epenthesis
from hfst.libhfst import replace_leftmost_longest_match
from hfst.libhfst import replace_leftmost_shortest_match
from hfst.libhfst import replace_rightmost_longest_match
from hfst.libhfst import replace_rightmost_shortest_match
from hfst.libhfst import REPL_DOWN
from hfst.libhfst import REPL_LEFT
from hfst.libhfst import REPL_RIGHT
from hfst.libhfst import REPL_UP
from hfst.libhfst import Rule


# these functions had to be renamed in the swig interface
# to prevent name collision
from hfst.libhfst import xerox_replace_left as replace_left
from hfst.libhfst import xerox_restriction as restriction


class ReplaceType:
    """
    Replace type in Xerox-type rules.

    Attributes:

        REPL_UP:      Match contexts on input level
        REPL_DOWN:    Match contexts on output level
        REPL_RIGHT:   Match left contexts on input level and right contexts on output level
        REPL_LEFT:    Match left contexts on output level and right contexts on input level

    """
    REPL_UP = hfst.libhfst.REPL_UP
    REPL_DOWN = hfst.libhfst.REPL_DOWN
    REPL_RIGHT = hfst.libhfst.REPL_RIGHT
    REPL_LEFT = hfst.libhfst.REPL_LEFT
