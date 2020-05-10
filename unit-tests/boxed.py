#!/usr/bin/env python3

"""
Multi-Independent optimization unit-test.
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
    "int"  : (),                    # (name, ...)
    "rational" : ("x", "y", "z"),   # (name, ...)
    "bv" : (),                      # ((name, width), ... )
    "fp" : ()                       # ((name, ebits, sbits), ... )
}

HARD = ["(<= 42 x)", "(<= y x)", "(< z 50)"]

SOFT = {}

###
### BOXED UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "x") as obj1, \
             create_maximize(env, "y") as obj2, \
             create_maximize(env, "z") as obj3:

            assert_objective(env, obj1)
            assert_objective(env, obj2)
            assert_objective(env, obj3)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (x 42)
#   (y +oo)
#   (z (- 50 epsilon))
# )
