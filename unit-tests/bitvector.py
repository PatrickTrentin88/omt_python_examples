#!/usr/bin/env python3

"""
Bit-Vector unit-test.
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
    "model_generation" : "true"
}

DECLS = {
    "bool" : (),        # (name, ...)
    "int"  : (),        # (name, ...)
    "rational" : (),    # (name, ...)
    "bv" : (("x", 8),), # ((name, width), ... )
    "fp" : ()           # ((name, ebits, sbits), ... )
}

HARD = [\
"""(or
    (and (bvsle ((_ to_bv 8) 120) x)
         (bvsle x ((_ to_bv 8) 120))
    )
    (and (bvsle ((_ to_bv 8) 97) x)
         (bvsle x ((_ to_bv 8) 97))
    )
    (and (bvsle ((_ to_bv 8) 54) x)
         (bvsle x ((_ to_bv 8) 54))
    )
    (and (bvsle ((_ to_bv 8) 32) x)
         (bvsle x ((_ to_bv 8) 32))
    )
    (and (bvsle ((_ to_bv 8) 22) x)
         (bvsle x ((_ to_bv 8) 22))
    )
    (and (bvsle ((_ to_bv 8) 11) x)
         (bvsle x ((_ to_bv 8) 11))
    )
    (and (bvsle ((_ to_bv 8) 8) x)
         (bvsle x ((_ to_bv 8) 8))
    )
    (and (bvsle ((_ to_bv 8) (- 7)) x)
         (bvsle x ((_ to_bv 8) (- 7)))
    )
    (and (bvsle ((_ to_bv 8) (- 16)) x)
         (bvsle x ((_ to_bv 8) (- 16)))
    )
    (and (bvsle ((_ to_bv 8) (- 105)) x)
         (bvsle x ((_ to_bv 8) (- 105)))
    )
)"""\
]

SOFT = {}

###
### BIT-VECTOR UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "x") as obj1, \
             create_minimize(env, "x", lower="((_ to_bv 8) (- 100))", signed=True) as obj2:
            assert_objective(env, obj1)
            assert_objective(env, obj2)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#     (x 8_8)
#     (x 240_8)
# )
