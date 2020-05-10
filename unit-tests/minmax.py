#!/usr/bin/env python3

"""
min-max unit-test.
"""

###
### SETUP PATHS
###

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCLUDE_DIR = os.path.join(BASE_DIR, '..', 'include')
LIB_DIR = os.path.join(BASE_DIR, '..', 'lib')
sys.path.append(INCLUDE_DIR)
sys.path.append(LIB_DIR)

################################################################################
################################################################################
################################################################################

from wrapper import * # pylint: disable=unused-wildcard-import,wildcard-import

###
### DATA
###

OPTIONS = {
    "opt.priority"     : "box",
}

DECLS = {
    "bool" : (),                    # (name, ...)
    "int"  : ("l0", "l1", "l2"),    # (name, ...)
    "rational" : (),                # (name, ...)
    "bv" : (),                      # ((name, width), ... )
    "fp" : ()                       # ((name, ebits, sbits), ... )
}

HARD = [
    "(< 10 l0)",
    "(< l2 l1)",
    "(< 14 l2)",
]

SOFT = {}

###
### MINMAX UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minmax(env, ["l0", "l1", "l2"]) as obj:

            assert_objective(env, obj)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (minmax 16)
# )
