#!/usr/bin/env python3

"""
Floating-Point unit-test.
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
    "model_generation" : "true",
    "printer.fp_number_format" : "1",
}

DECLS = {
    "bool" : (),        # (name, ...)
    "int"  : (),        # (name, ...)
    "rational" : (),    # (name, ...)
    "bv" : (),          # ((name, width), ... )
    "fp" : (            # ((name, ebits, sbits), ... )
        ("x0", 8, 23),
        ("x1", 8, 23),
        ("x2", 8, 23),
        ("x3", 8, 23),
    )
}

_M_INF = "(fp #b1 #b11111111 #b00000000000000000000000)"
_M_TEN = "(fp #b1 #b10000010 #b01000000000000000000000)"
_ZERO = "(fp #b0 #b00000000 #b00000000000000000000000)"
_P_TEN = "(fp #b0 #b10000010 #b01000000000000000000000)"
_P_INF = "(fp #b0 #b11111111 #b00000000000000000000000)"

HARD = (
    "(fp.leq {} x0)".format(_M_TEN),
    "(fp.leq x0 {})".format(_P_TEN),
    "(= x1 {})".format(_ZERO),
    "(= x2 (_ NaN 8 24))",
    "(fp.leq {} x3)".format(_M_INF),
    "(fp.leq x3 {})".format(_P_INF),
)

SOFT = {}

###
### FLOATING-POINT UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "x0") as obj1, \
             create_maximize(env, "x0") as obj2, \
             create_minimize(env, "x1") as obj3, \
             create_minimize(env, "x2") as obj4, \
             create_minimize(env, "x3") as obj5, \
             create_maximize(env, "x3") as obj6:

            assert_objective(env, obj1)
            assert_objective(env, obj2)
            assert_objective(env, obj3)
            assert_objective(env, obj4)
            assert_objective(env, obj5)
            assert_objective(env, obj6)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (x0 3240099840_8_23)
#   (x0 1092616192_8_23)
#   (x1 0_8_23)
#   (x2 4286578689_8_23)    ; (_ NaN 8 24)
#   (x3 -oo)
#   (x3 +oo)
# )
