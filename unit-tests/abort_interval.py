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
# # obj(.cost_0) - search end: sat_approx
# sat
# (objectives
#   (objective 161/5), termination threshold, range: [ 23, 161/5 ]
# )
