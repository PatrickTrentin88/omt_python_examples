#!/usr/bin/env python3

"""
All-Sat unit-test.
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
    "opt.priority"     : "lex",
    "model_generation" : "true",
}

DECLS = {
    "bool" : ("a", "b", "c", "d", "e"), # (name, ...)
    "int"  : ("y"),                     # (name, ...)
    "rational" : ("x"),                 # (name, ...)
    "bv" : (),                          # ((name, width), ... )
    "fp" : ()                           # ((name, ebits, sbits), ... )
}

HARD = [
    "(= (> (+ x y) 0) a)",
    "(= (< (+ (* 2 x) (* 3 y)) (- 10)) c)",
    "(or a b)",
    "(or c d)",
    "(=> e (< 10 x))",
    "(=> (< 10 x) e)",
    "(<= x 100)",
    "(<= y 100)",
]

SOFT = {}

###
### ALLSAT UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_maximize(env, "x") as obj1, \
             create_maximize(env, "y") as obj2:
            assert_objective(env, obj1)
            assert_objective(env, obj2)

            solve_all_sat(env, ["a", "b", "e"])

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (x 100)
#   (y 100)
# )
# sat
#   a : True
#   b : True
#   e : True
# sat
#   a : True
#   b : False
#   e : True
