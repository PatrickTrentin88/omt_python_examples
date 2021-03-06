#!/usr/bin/env python3

"""
MaxSMT unit-test.
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
    "opt.maxsmt_engine" : "maxres",
    "model_generation"  : "true",
}

DECLS = {
    "bool" : (),            # (name, ...)
    "int"  : ("x", "y"),    # (name, ...)
    "rational" : (),        # (name, ...)
    "bv" : (),              # ((name, width), ... )
    "fp" : ()               # ((name, ebits, sbits), ... )
}

HARD = [
    "(= x (- y))"
]

SOFT = {
    "goal" : (
        ("(< x 0)", "1"),
        ("(< x y)", "1"),
        ("(< y 0)", "1")
    )
}

###
### MAXSMT UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "goal") as obj:

            assert_objective(env, obj)
            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (goal 1)
# )
