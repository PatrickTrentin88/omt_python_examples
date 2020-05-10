#!/usr/bin/env python3

"""
Lexicographic OMT unit-test.
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
    "bool" : ("s1", "s2", "s3", "s4"),              # (name, ...)
    "int"  : (),                                    # (name, ...)
    "rational" : ("q1", "q2", "q3", "q4", "cost"),  # (name, ...)
    "bv" : (),                                      # ((name, width), ... )
    "fp" : ()                                       # ((name, ebits, sbits), ... )
}

HARD = [
    # set goods quantity
    "(= 250 (+ q1 q2 q3 q4))",
    # set goods offered by each supplier
    "(or (= q1 0) (and (<= 50 q1) (<= q1 250)))",
    "(or (= q2 0) (and (<= 100 q2) (<= q2 150)))",
    "(or (= q3 0) (and (<= 100 q3) (<= q3 100)))",
    "(or (= q4 0) (and (<= 50 q4) (<= q4 100)))",
    # supplier is used if sends more than zero items
    "(=> s1 (not (= q1 0)))",
    "(=> s2 (not (= q2 0)))",
    "(=> s3 (not (= q3 0)))",
    "(=> s4 (not (= q4 0)))",
]

SOFT = {
    "unused_suppliers" : (
        ("s1", "1"),
        ("s2", "1"),
        ("s3", "1"),
        ("s4", "1"),
    )
}

###
### LEXICOGRAPHIC UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "(+ (* q1 23) (* q2 21) (* q3 20) (* q4 10))") as obj1, \
             create_minimize(env, "unused_suppliers") as obj2:
            assert_objective(env, obj1)
            assert_objective(env, obj2)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   ((`+_rat` (`*_rat` 10 q4) (`+_rat` (`*_rat` 20 q3) \
#             (`+_rat` (`*_rat` 23 q1) (`*_rat` 21 q2)))) 4150)
#   (unused_suppliers 1)
# )
