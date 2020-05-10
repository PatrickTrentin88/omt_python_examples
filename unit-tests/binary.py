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

        with create_minimize(env, "objective") as obj:
            assert_objective(env, obj)

            solve(env)
            get_objectives_pretty(env)


#
## EXPECTED OUTPUT
#
# # obj(objective) := objective
# # obj(objective) - search start: [ (- oo), oo ]
# # obj(objective) - linear step: 1
# # obj(objective) -  new: 75
# # obj(objective) -  update upper: [ (- oo), 75 ]
# # obj(objective) - binary step: 1
# # obj(objective) - pivot: (not (<= (to_real 0) objective))
# # obj(objective) -  update lower: [ 0, 75 ]
# # obj(objective) - binary step: 2
# # obj(objective) - pivot: (not (<= (/ 75 2) objective))
# # obj(objective) -  new: (/ 112 3)
# # obj(objective) -  update upper: [ 0, (/ 112 3) ]
# # obj(objective) - binary step: 3
# # obj(objective) - pivot: (not (<= (/ 56 3) objective))
# # obj(objective) -  update lower: [ (/ 56 3), (/ 112 3) ]
# # obj(objective) - binary step: 4
# # obj(objective) - pivot: (not (<= (to_real 28) objective))
# # obj(objective) -  new: (/ 223 8)
# # obj(objective) -  update upper: [ (/ 56 3), (/ 223 8) ]
# # obj(objective) - binary step: 5
# # obj(objective) - pivot: (not (<= (/ 1117 48) objective))
# # obj(objective) -  update lower: [ (/ 1117 48), (/ 223 8) ]
# # obj(objective) - binary step: 6
# # obj(objective) - pivot: (not (<= (/ 2455 96) objective))
# # obj(objective) -  update lower: [ (/ 2455 96), (/ 223 8) ]
# # obj(objective) - linear step: 2
# # obj(objective) -  new: (/ 250 9)
# # obj(objective) -  update upper: [ (/ 2455 96), (/ 250 9) ]
# # obj(objective) - binary step: 7
# # obj(objective) - pivot: (not (<= (/ 15365 576) objective))
# # obj(objective) -  update lower: [ (/ 15365 576), (/ 250 9) ]
# # obj(objective) - binary step: 8
# # obj(objective) - pivot: (not (<= (/ 3485 128) objective))
# # obj(objective) -  new: (/ 245 9)
# # obj(objective) -  update upper: [ (/ 15365 576), (/ 245 9) ]
# # obj(objective) - binary step: 9
# # obj(objective) - pivot: (not (<= (/ 31045 1152) objective))
# # obj(objective) -  update lower: [ (/ 31045 1152), (/ 245 9) ]
# # obj(objective) - binary step: 10
# # obj(objective) - pivot: (not (<= (/ 62405 2304) objective))
# # obj(objective) -  new: 27
# # obj(objective) -  update upper: [ (/ 31045 1152), 27 ]
# # obj(objective) - binary step: 11
# # obj(objective) - pivot: (not (<= (/ 62149 2304) objective))
# # obj(objective) -  update lower: [ (/ 62149 2304), 27 ]
# # obj(objective) - binary step: 12
# # obj(objective) - pivot: (not (<= (/ 124357 4608) objective))
# # obj(objective) -  update lower: [ (/ 124357 4608), 27 ]
# # obj(objective) - linear step: 3
# # obj(objective) - search end: sat_optimal
# # obj(objective) -  update lower: [ 27, 27 ]
# sat
# (objectives
#   (objective 27)
# )
