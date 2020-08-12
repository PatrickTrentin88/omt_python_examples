#!/usr/bin/env python3

"""
Priority OMT unit-test.
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
    "model_generation" : "true",
    "opt.priority"     : "box",
    "opt.par.mode"     : "incremental"
}

DECLS = {
    "bool" : (),                # (name, ...)
    "int"  : (),                # (name, ...)
    "rational" : ("a", "b"),    # (name, ...)
    "bv" : (),                  # ((name, width), ... )
    "fp" : ()                   # ((name, ebits, sbits), ... )
}

HARD = [
    """(or
        (and (= a 1) (= b 1))
        (and (= a 2) (= b 1))
        (and (= a 1) (= b 2))
        (and (= a 2) (= b 2))
        (and (= a 3) (= b 1))
        (and (= a 1) (= b 3))
    )"""
]

SOFT = {}

###
### PRIORITY UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_maximize(env, "a") as obj1, \
             create_maximize(env, "b") as obj2:
            assert_objective(env, obj1)
            assert_objective(env, obj2)

            print("=== BOXED OPTIMIZATION ===")
            msat_set_opt_priority(env, "box")
            solve(env)
            get_objectives_pretty(env)

            print("=== LEXICOGRAPHIC OPTIMIZATION ===")
            msat_set_opt_priority(env, "lex")
            solve(env)
            get_objectives_pretty(env)

            print("=== PARETO OPTIMIZATION ===")
            msat_set_opt_priority(env, "par")
            while solve(env) > 0:
                dump_model(env)


#
## EXPECTED OUTPUT
#
# === BOXED OPTIMIZATION ===
# sat
# (objectives
# 	(a 3)
# 	(b 3)
# )
# === LEXICOGRAPHIC OPTIMIZATION ===
# sat
# (objectives
# 	(a 3)
# 	(b 1)
# )
# === PARETO OPTIMIZATION ===
# sat
# 	a : 3
# 	b : 1
# sat
# 	a : 1
# 	b : 3
# sat
# 	a : 2
# 	b : 2
# unsat
