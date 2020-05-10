#!/usr/bin/env python3

"""
Simple OMT problem unit-test.
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
    "bool" : ("B1", ),              # (name, ...)
    "int"  : ("x1", "x2", "cost"),  # (name, ...)
    "rational" : (),                # (name, ...)
    "bv" : (),                      # ((name, width), ... )
    "fp" : ()                       # ((name, ebits, sbits), ... )
}

HARD = [
    "(<= 0 x1)", "(<= x1 10)",
    "(<= 0 x2)", "(<= x2 10)",
    "(not (= x1 x2))", "B1",
    "(=> B1 (< x1 x2))",
    "(=> (not B1) (< x2 x1))",
    "(= cost (+ x1 x2))"
]

SOFT = {}

###
### SIMPLE OMT PROBLEM UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_maximize(env, "cost") as obj1, \
             create_minimize(env, "cost") as obj2, \
             create_maxmin(env, ["x1", "x2"]) as obj3:

            push(env)
            assert_objective(env, obj1)
            solve(env)
            dump_model(env)
            pop(env)

            push(env)
            assert_objective(env, obj2)
            solve(env)
            dump_model(env)
            pop(env)

            push(env)
            assert_objective(env, obj3)
            assert_string_formula(env, "(or (<= x1 7) (<= x1 3))")
            solve(env)
            dump_model(env)
            pop(env)

#
## EXPECTED OUTPUT
#
# sat
#   B1 : `true`
#   x1 : 9
#   x2 : 10
#   cost : 19
# sat
#   B1 : `true`
#   x1 : 0
#   x2 : 1
#   cost : 1
# sat
#   B1 : `true`
#   x1 : 7
#   x2 : 8
#   cost : 15
#   minmax : 7
