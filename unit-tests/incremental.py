#!/usr/bin/env python3

"""
incremental OMT unit-test.
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

OPTIONS = {}

DECLS = {
    "bool" : (),        # (name, ...)
    "int"  : (),        # (name, ...)
    "rational" : ("x"), # (name, ...)
    "bv" : (),          # ((name, width), ... )
    "fp" : (),          # ((name, ebits, sbits), ... )
}

HARD = []

SOFT = {}

###
### INCREMENTAL UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)

        with create_minimize(env, "x") as obj:

            push(env)
            assert_objective(env, obj)
            assert_string_formula(env, "(<= 5 x)")
            solve(env)
            get_objectives_pretty(env)
            pop(env)

            push(env)
            assert_objective(env, obj)
            solve(env)
            get_objectives_pretty(env)
            pop(env)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (x 5)
# )
# sat
# (objectives
#   (x -oo)
# )
# sat
# (objectives
# )
