#!/usr/bin/env python3

"""
binary search unit-test.
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
    "opt.verbose"               : "true",
    "opt.strategy"              : "bin",
    "opt.bin.first_step_linear" : "false",
    "opt.bin.max_consecutive"   : "2",
    "opt.bin.pivot_position"    : "0.5",
}

###
### BINARY SEARCH UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        # load non-trivial formula directly from file
        with open(os.path.join(BASE_DIR, 'smt2', 'bacp-19.smt2'), 'r') as f:
            TERM = msat_from_smtlib2(env, f.read())
            assert not MSAT_ERROR_TERM(TERM)
            msat_assert_formula(env, TERM)

        with create_minimize(env, "objective", lower="23", upper="100") as obj:
            assert_objective(env, obj)

            solve(env)
            get_objectives_pretty(env)


#
## EXPECTED OUTPUT
#
# # obj(.cost_0) := objective
# # obj(.cost_0) - search start: [ 23, 100 ]
# # obj(.cost_0) - binary step: 1
# # obj(.cost_0) - pivot: (not (<= (/ 123 2) .cost_0))
# # obj(.cost_0) -  new: 112/3
# # obj(.cost_0) -  update upper: [ 23, 112/3 ]
# # obj(.cost_0) - binary step: 2
# # obj(.cost_0) - pivot: (not (<= (/ 181 6) .cost_0))
# # obj(.cost_0) -  new: 30
# # obj(.cost_0) -  update upper: [ 23, 30 ]
# # obj(.cost_0) - binary step: 3
# # obj(.cost_0) - pivot: (not (<= (/ 53 2) .cost_0))
# # obj(.cost_0) -  update lower: [ 53/2, 30 ]
# # obj(.cost_0) - binary step: 4
# # obj(.cost_0) - pivot: (not (<= (/ 113 4) .cost_0))
# # obj(.cost_0) -  new: 197/7
# # obj(.cost_0) -  update upper: [ 53/2, 197/7 ]
# # obj(.cost_0) - binary step: 5
# # obj(.cost_0) - pivot: (not (<= (/ 765 28) .cost_0))
# # obj(.cost_0) -  new: 109/4
# # obj(.cost_0) -  update upper: [ 53/2, 109/4 ]
# # obj(.cost_0) - binary step: 6
# # obj(.cost_0) - pivot: (not (<= (/ 215 8) .cost_0))
# # obj(.cost_0) -  update lower: [ 215/8, 109/4 ]
# # obj(.cost_0) - binary step: 7
# # obj(.cost_0) - pivot: (not (<= (/ 433 16) .cost_0))
# # obj(.cost_0) -  new: 27
# # obj(.cost_0) -  update upper: [ 215/8, 27 ]
# # obj(.cost_0) - binary step: 8
# # obj(.cost_0) - pivot: (not (<= (/ 431 16) .cost_0))
# # obj(.cost_0) -  update lower: [ 431/16, 27 ]
# # obj(.cost_0) - binary step: 9
# # obj(.cost_0) - pivot: (not (<= (/ 863 32) .cost_0))
# # obj(.cost_0) -  update lower: [ 863/32, 27 ]
# # obj(.cost_0) - linear step: 1
# # obj(.cost_0) - search end: sat_optimal
# # obj(.cost_0) -  update lower: [ 27, 27 ]
# sat
# (objectives
#   (objective 27)
# )
