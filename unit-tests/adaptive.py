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
# # obj(objective) - linear step: 2
# # obj(objective) -  new: 69
# # obj(objective) -  update upper: [ (- oo), 69 ]
# # obj(objective) - binary step: 1
# # obj(objective) - pivot: (not (<= (to_real 0) objective))
# # obj(objective) -  update lower: [ 0, 69 ]
# # obj(objective) - binary step: 2
# # obj(objective) - pivot: (not (<= (/ 69 2) objective))
# # obj(objective) -  new: (/ 137 4)
# # obj(objective) -  update upper: [ 0, (/ 137 4) ]
# # obj(objective) - linear step: 3
# # obj(objective) -  new: 34
# # obj(objective) -  update upper: [ 0, 34 ]
# # obj(objective) - binary step: 3
# # obj(objective) - pivot: (not (<= (to_real 17) objective))
# # obj(objective) -  update lower: [ 17, 34 ]
# # obj(objective) - binary step: 4
# # obj(objective) - pivot: (not (<= (/ 51 2) objective))
# # obj(objective) -  update lower: [ (/ 51 2), 34 ]
# # obj(objective) - binary step: 5
# # obj(objective) - pivot: (not (<= (/ 119 4) objective))
# # obj(objective) -  new: (/ 59 2)
# # obj(objective) -  update upper: [ (/ 51 2), (/ 59 2) ]
# # obj(objective) - linear step: 4
# # obj(objective) -  new: (/ 265 9)
# # obj(objective) -  update upper: [ (/ 51 2), (/ 265 9) ]
# # obj(objective) - binary step: 6
# # obj(objective) - pivot: (not (<= (/ 989 36) objective))
# # obj(objective) -  new: (/ 247 9)
# # obj(objective) -  update upper: [ (/ 51 2), (/ 247 9) ]
# # obj(objective) - binary step: 7
# # obj(objective) - pivot: (not (<= (/ 953 36) objective))
# # obj(objective) -  update lower: [ (/ 953 36), (/ 247 9) ]
# # obj(objective) - binary step: 8
# # obj(objective) - pivot: (not (<= (/ 647 24) objective))
# # obj(objective) -  update lower: [ (/ 647 24), (/ 247 9) ]
# # obj(objective) - binary step: 9
# # obj(objective) - pivot: (not (<= (/ 3917 144) objective))
# # obj(objective) -  new: 27
# # obj(objective) -  update upper: [ (/ 647 24), 27 ]
# # obj(objective) - binary step: 10
# # obj(objective) - pivot: (not (<= (/ 1295 48) objective))
# # obj(objective) -  update lower: [ (/ 1295 48), 27 ]
# # obj(objective) - binary step: 11
# # obj(objective) - pivot: (not (<= (/ 2591 96) objective))
# # obj(objective) -  update lower: [ (/ 2591 96), 27 ]
# # obj(objective) - binary step: 12
# # obj(objective) - pivot: (not (<= (/ 5183 192) objective))
# # obj(objective) -  update lower: [ (/ 5183 192), 27 ]
# # obj(objective) - binary step: 13
# # obj(objective) - pivot: (not (<= (/ 10367 384) objective))
# # obj(objective) -  update lower: [ (/ 10367 384), 27 ]
# # obj(objective) - binary step: 14
# # obj(objective) - pivot: (not (<= (/ 20735 768) objective))
# # obj(objective) -  update lower: [ (/ 20735 768), 27 ]
# # obj(objective) - linear step: 5
# # obj(objective) - search end: sat_optimal
# # obj(objective) -  update lower: [ 27, 27 ]
# sat
# (objectives
#   (objective 27)
# )
