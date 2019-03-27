#!/usr/bin/env python3

"""
adaptive search unit-test.
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
    "opt.strategy"              : "ada",
    "opt.bin.first_step_linear" : "false",
    "opt.bin.max_consecutive"   : "5",
    "opt.bin.pivot_position"    : "0.5",
}

###
### ADAPTIVE SEARCH UNIT-TEST
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
# # obj(.cost_0) - linear step: 1
# # obj(.cost_0) -  new: 46
# # obj(.cost_0) -  update upper: [ 23, 46 ]
# # obj(.cost_0) - binary step: 1
# # obj(.cost_0) - pivot: (not (<= (/ 69 2) .cost_0))
# # obj(.cost_0) -  new: 103/3
# # obj(.cost_0) -  update upper: [ 23, 103/3 ]
# # obj(.cost_0) - binary step: 2
# # obj(.cost_0) - pivot: (not (<= (/ 86 3) .cost_0))
# # obj(.cost_0) -  new: 251/9
# # obj(.cost_0) -  update upper: [ 23, 251/9 ]
# # obj(.cost_0) - binary step: 3
# # obj(.cost_0) - pivot: (not (<= (/ 229 9) .cost_0))
# # obj(.cost_0) -  update lower: [ 229/9, 251/9 ]
# # obj(.cost_0) - binary step: 4
# # obj(.cost_0) - pivot: (not (<= (/ 80 3) .cost_0))
# # obj(.cost_0) -  update lower: [ 80/3, 251/9 ]
# # obj(.cost_0) - binary step: 5
# # obj(.cost_0) - pivot: (not (<= (/ 491 18) .cost_0))
# # obj(.cost_0) -  new: 245/9
# # obj(.cost_0) -  update upper: [ 80/3, 245/9 ]
# # obj(.cost_0) - binary step: 6
# # obj(.cost_0) - pivot: (not (<= (/ 485 18) .cost_0))
# # obj(.cost_0) -  update lower: [ 485/18, 245/9 ]
# # obj(.cost_0) - binary step: 7
# # obj(.cost_0) - pivot: (not (<= (/ 325 12) .cost_0))
# # obj(.cost_0) -  new: 27
# # obj(.cost_0) -  update upper: [ 485/18, 27 ]
# # obj(.cost_0) - binary step: 8
# # obj(.cost_0) - pivot: (not (<= (/ 971 36) .cost_0))
# # obj(.cost_0) -  update lower: [ 971/36, 27 ]
# # obj(.cost_0) - binary step: 9
# # obj(.cost_0) - pivot: (not (<= (/ 1943 72) .cost_0))
# # obj(.cost_0) -  update lower: [ 1943/72, 27 ]
# # obj(.cost_0) - binary step: 10
# # obj(.cost_0) - pivot: (not (<= (/ 3887 144) .cost_0))
# # obj(.cost_0) -  update lower: [ 3887/144, 27 ]
# # obj(.cost_0) - binary step: 11
# # obj(.cost_0) - pivot: (not (<= (/ 7775 288) .cost_0))
# # obj(.cost_0) -  update lower: [ 7775/288, 27 ]
# # obj(.cost_0) - binary step: 12
# # obj(.cost_0) - pivot: (not (<= (/ 15551 576) .cost_0))
# # obj(.cost_0) -  update lower: [ 15551/576, 27 ]
# # obj(.cost_0) - linear step: 2
# # obj(.cost_0) - search end: sat_optimal
# # obj(.cost_0) -  update lower: [ 27, 27 ]
# sat
# (objectives
#   (objective 27)
# )
