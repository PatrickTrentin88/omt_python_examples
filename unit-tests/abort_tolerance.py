#!/usr/bin/env python3

"""
abort tolerance unit-test.
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
    "model_generation"    : "true",
    "opt.verbose"         : "true",
    "opt.abort_tolerance" : "0.09",
}

###
### ABORT TOLERANCE UNIT-TEST
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

#            load_model(env, obj)
#            dump_model(env)


#
## EXPECTED OUTPUT
#
# # obj(.cost_0) := objective
# # obj(.cost_0) - search start: [ 23, 100 ]
# # obj(.cost_0) - linear step: 1
# # obj(.cost_0) -  new: 46
# # obj(.cost_0) -  update upper: [ 23, 46 ]
# # obj(.cost_0) - linear step: 2
# # obj(.cost_0) -  new: 130/3
# # obj(.cost_0) -  update upper: [ 23, 130/3 ]
# # obj(.cost_0) - linear step: 3
# # obj(.cost_0) -  new: 40
# # obj(.cost_0) -  update upper: [ 23, 40 ]
# # obj(.cost_0) - linear step: 4
# # obj(.cost_0) -  new: 119/3
# # obj(.cost_0) -  update upper: [ 23, 119/3 ]
# # obj(.cost_0) - linear step: 5
# # obj(.cost_0) -  new: 112/3
# # obj(.cost_0) -  update upper: [ 23, 112/3 ]
# # obj(.cost_0) - linear step: 6
# # obj(.cost_0) -  new: 104/3
# # obj(.cost_0) -  update upper: [ 23, 104/3 ]
# # obj(.cost_0) - linear step: 7
# # obj(.cost_0) -  new: 34
# # obj(.cost_0) -  update upper: [ 23, 34 ]
# # obj(.cost_0) - linear step: 8
# # obj(.cost_0) -  new: 133/4
# # obj(.cost_0) -  update upper: [ 23, 133/4 ]
# # obj(.cost_0) - linear step: 9
# # obj(.cost_0) -  new: 161/5
# # obj(.cost_0) -  update upper: [ 23, 161/5 ]
# # obj(.cost_0) - linear step: 10
# # obj(.cost_0) -  new: 32
# # obj(.cost_0) -  update upper: [ 23, 32 ]
# # obj(.cost_0) - linear step: 11
# # obj(.cost_0) -  new: 158/5
# # obj(.cost_0) -  update upper: [ 23, 158/5 ]
# # obj(.cost_0) - linear step: 12
# # obj(.cost_0) -  new: 247/8
# # obj(.cost_0) -  update upper: [ 23, 247/8 ]
# # obj(.cost_0) - linear step: 13
# # obj(.cost_0) -  new: 123/4
# # obj(.cost_0) -  update upper: [ 23, 123/4 ]
# # obj(.cost_0) - linear step: 14
# # obj(.cost_0) -  new: 61/2
# # obj(.cost_0) -  update upper: [ 23, 61/2 ]
# # obj(.cost_0) - linear step: 15
# # obj(.cost_0) -  new: 91/3
# # obj(.cost_0) -  update upper: [ 23, 91/3 ]
# # obj(.cost_0) - linear step: 16
# # obj(.cost_0) -  new: 181/6
# # obj(.cost_0) -  update upper: [ 23, 181/6 ]
# # obj(.cost_0) - linear step: 17
# # obj(.cost_0) -  new: 241/8
# # obj(.cost_0) -  update upper: [ 23, 241/8 ]
# # obj(.cost_0) - linear step: 18
# # obj(.cost_0) -  new: 88/3
# # obj(.cost_0) -  update upper: [ 23, 88/3 ]
# # obj(.cost_0) - search end: sat_approx
# sat
# (objectives
#   (objective 88/3), termination threshold, range: [ 23, 88/3 ]
# )
