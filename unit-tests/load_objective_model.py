#!/usr/bin/env python3

"""
load-objective-model unit-test.
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
}

DECLS = {
    "bool" : (),                # (name, ...)
    "int"  : ("x", "y", "z"),   # (name, ...)
    "rational" : (),            # (name, ...)
    "bv" : (),                  # ((name, width), ... )
    "fp" : ()                   # ((name, ebits, sbits), ... )
}

HARD = [
    "(<= 3 x)",
    "(<= x 5)",
    "(<= 10 z)",
    "(<= z 20)",
    "(= y (+ (* 2 x) z))",
]

SOFT = {}

###
### LOAD_OBJECTIVE_MODEL UNIT-TEST
###

def problem(incfg):
    """
    A simple OMT problem.

    :param incfg: the input configuration.
    """
    with create_env(incfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "x") as obj1, \
             create_maximize(env, "y") as obj2:
            assert_objective(env, obj1)
            assert_objective(env, obj2)

            msat_set_option(cfg, "opt.priority", "box")
            solve(env)
            get_objectives_pretty(env)

            print("\nModel: minimize x")
            load_model(env, obj1)
            dump_model(env)

            print("\nModel: maximize y")
            load_model(env, obj2)
            dump_model(env)

# BOXED OPTIMIZATION + 2 MODELS
with create_config(OPTIONS) as cfg:
    msat_set_option(cfg, "opt.priority", "box")
    problem(cfg)

# LEXICOGRAPHIC OPTIMIZATION + 2 MODELS
with create_config(OPTIONS) as cfg:
    msat_set_option(cfg, "opt.priority", "lex")
    problem(cfg)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (x 3)
#   (y 30)
# )
#
# Model: minimize x
#   x : 3
#   y : 16
#   z : 10
#
# Model: maximize y
#   x : 5
#   y : 30
#   z : 20
# sat
# (objectives
#   (x 3)
#   (y 26)
# )
#
# Model: minimize x
#   x : 3
#   y : 16
#   z : 10
#
# Model: maximize y
#   x : 3
#   y : 26
#   z : 20
