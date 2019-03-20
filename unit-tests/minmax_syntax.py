#!/usr/bin/env python3

"""
min-max syntax unit-test.
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
}

DECLS = {
    "bool" : (),
    "int"  : ("i"),
    "rational" : ("r"),
    "bv" : (
        ("b8", 8),
        ("b4", 4)
    ),
    "fp" : (
        ("f8", 3, 4),
        ("f16", 6, 9)
    )
}

HARD = [
    "(< r 14)",
    "(< i 13)",
    "(bvule b8 #b00001100)",
    "(bvsle b4 #b0001)",
    "(fp.leq f8 (fp #b0 #b010 #b0010))",
    "(not (fp.isNaN f8))",
    "(not (fp.isInfinite f8))",
    "(not (fp.isNaN f16))",
    "(not (fp.isInfinite f16))",
]

SOFT = {}

###
### MINMAX SYNTAX UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minmax(env, ["r", "(to_real i)", "(ubv_to_int b8)"]) as obj1, \
             create_minmax(env, ["(to_int r)", "i", "(sbv_to_int b8)"]) as obj2, \
             create_minmax(env, ["((_ extract 3 0) b8)", "b4"]) as obj3, \
             create_minmax(env, ["((_ to_bv 8) (to_int r))",
                                 "((_ to_bv 8) i)", "b8",
                                 "((_ fp.to_ubv 8) RNE f8)",
                                 "((_ zero_extend 4) b4)"]) as obj4, \
             create_minmax(env, ["((_ to_bv 8) (to_int r))",
                                 "((_ to_bv 8) i)", "b8",
                                 "((_ fp.to_sbv 8) RNE f8)",
                                 "((_ sign_extend 4) b4)"], signed=True) as obj5, \
             create_minmax(env, ["((_ to_fp 3 5) RNE b8)",
                                 "((_ to_fp_unsigned 3 5) RNE b4)", "f8",
                                 "((_ to_fp 3 5) RNE f16)"]) as obj6:
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
#   (minmax 12)
#   (minmax_0 12)
#   (minmax_1 12_4)
#   (minmax_2 12_8)
#   (minmax_3 1_8)
#   (minmax_4 34_3_4)
# )
