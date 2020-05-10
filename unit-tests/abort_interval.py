#!/usr/bin/env python3

"""
abort interval unit-test.
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
    "model_generation"   : "true",
    "opt.verbose"        : "true",
    "opt.abort_interval" : "10",
}

###
### ABORT INTERVAL UNIT-TEST
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

#            load_model(env, obj)
#            dump_model(env)


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
# # obj(objective) - linear step: 2
# # obj(objective) -  new: 69
# # obj(objective) -  update upper: [ 0, 69 ]
# # obj(objective) - binary step: 2
# # obj(objective) - pivot: (not (<= (/ 69 2) objective))
# # obj(objective) -  new: (/ 137 4)
# # obj(objective) -  update upper: [ 0, (/ 137 4) ]
# # obj(objective) - binary step: 3
# # obj(objective) - pivot: (not (<= (/ 137 8) objective))
# # obj(objective) -  update lower: [ (/ 137 8), (/ 137 4) ]
# # obj(objective) - linear step: 3
# # obj(objective) -  new: 34
# # obj(objective) -  update upper: [ (/ 137 8), 34 ]
# # obj(objective) - binary step: 4
# # obj(objective) - pivot: (not (<= (/ 409 16) objective))
# # obj(objective) -  update lower: [ (/ 409 16), 34 ]
# # obj(objective) - search end: sat_approx
# sat
# (objectives
#   (objective 34), termination threshold, range: [ 409/16, 34 ]
# )
