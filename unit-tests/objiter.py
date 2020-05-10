#!/usr/bin/env python3

"""
objective iterator and objective values unit-test.
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
    "bool" : (),                                    # (name, ...)
    "int"  : (),                                    # (name, ...)
    "rational" : ("a", "b", "c", "d", "eps", "oo"), # (name, ...)
    "bv" : (),                                      # ((name, width), ... )
    "fp" : ()                                       # ((name, ebits, sbits), ... )
}

HARD = [
    "(<= 42 a)",
    "(< b 3)",
]

SOFT = {}


###
### OBJITER UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "a") as obj1, \
             create_maximize(env, "b") as obj2, \
             create_minimize(env, "c") as obj3, \
             create_minimize(env, "d") as obj4:

            assert_objective(env, obj1)
            assert_objective(env, obj2)
            assert_objective(env, obj3)
            assert_objective(env, obj4)

            solve(env)

            print("\n\t### GET-OBJECTIVES ###")

            print("\n  -*- default approximation -*-")
            get_objectives(env)

            print("\n  -*- custom approximation -*-")
            INF = msat_from_string(env, "999999999999999999999")
            EPS = msat_from_string(env, "(/ 1 10000000000000000)")
            get_objectives(env, INF, EPS)

            print("\n  -*- symbolic with internal representation -*-")
            INF = msat_from_string(env, "oo")   # N.B.: already declared.
            EPS = msat_from_string(env, "eps")  # N.B.: already declared.
            get_objectives(env, INF, EPS)

            print("\n  -*- symbolic with pretty string -*-")
            get_objectives_pretty(env)

            print("\n\t### DUMP MODELS ###\n")
            dump_models(env)

#
## EXPECTED OUTPUT
#
# sat
#
#   ### GET-OBJECTIVES ###
#
#   -*- default approximation -*-
# (objectives
#   (a 42)
#   (b 2999999/1000000)
#   (c -1000000000)
#   (d -1000000000)
# )
#
#   -*- custom approximation -*-
# (objectives
#   (a 42)
#   (b 29999999999999999/10000000000000000)
#   (c -999999999999999999999)
#   (d -999999999999999999999)
# )
#
#   -*- symbolic with internal representation -*-
# (objectives
#   (a 42)
#   (b (`+_rat` 3 (`*_rat` -1 eps)))
#   (c (`*_rat` -1 oo))
#   (d (`*_rat` -1 oo))
# )
#
#   -*- symbolic with pretty string -*-
# (objectives
#   (a 42)
#   (b (- 3 epsilon))
#   (c -oo)
#   (d -oo)
# )
#
#   ### DUMP MODELS ###
#
# % Goal: a
# % Status: MSAT_OPT_SAT_OPTIMAL
# % (Finite) Model:
#   a : 42
#   b : 0
#   c : 1
#   d : 2
#
# % Goal: b
# % Status: MSAT_OPT_SAT_OPTIMAL
# % (Finite) Model:
#   a : 42
#   b : 2999999/1000000
#   c : -1000000000
#   d : -1000000000
#
# % Goal: c
# % Status: MSAT_OPT_SAT_OPTIMAL
# % (Finite) Model:
#   a : 42
#   b : 3999999/2000000
#   c : -1000000000
#   d : -221999989/2000000
#
# % Goal: d
# % Status: MSAT_OPT_SAT_OPTIMAL
# % (Finite) Model:
#   a : 42
#   b : 3999999/2000000
#   c : -1000000000
#   d : -1000000000
#
