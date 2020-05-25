#!/usr/bin/env python3

"""
Author: Kai Waelti, kai.waelti@pm.me

timeout benchmark file
inspired by Patrick Trentin' omt_python_examples
https://github.com/PatrickTrentin88/omt_python_examples
"""

# SETUP PATHS

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCLUDE_DIR = os.path.join(BASE_DIR, 'include')
LIB_DIR = os.path.join(BASE_DIR, 'lib')
sys.path.append(INCLUDE_DIR)
sys.path.append(LIB_DIR)

###############################################################################
###############################################################################
###############################################################################

from wrapper import * # pylint: disable=unused-wildcard-import,wildcard-import

# DATA

OPTIONS = {
    "model_generation": "true",
    "opt.soft_timeout": "false",
    "opt.verbose": "true",
}

filename: str = os.path.join(BASE_DIR, 'smt2-files', 'Mz1-noAbs', 'A004-dzn-fzn_v3.smt2')

# PROGRAM

with create_config(OPTIONS) as cfg:
    with create_env(cfg, optimizing=True) as env:
        with open(filename, 'r') as f:
            formula = msat_from_smtlib2(env, f.read())
            if (MSAT_ERROR_TERM(formula)):
                print(f'''Unable to parse {filename}''')
            msat_assert_formula(env, formula)

            # Set a timeout
            CALLBACK = Timer(3.0)
            msat_set_termination_test(env, CALLBACK)

            signed: bool = True

            try:
                tcf = string_to_term(env, 'obj')
                # TODO: Any way to add lower und upper bounds?
                obj = msat_make_minimize(env, tcf, signed)
                assert_objective(env, obj)
                solve(env)
                get_objectives_pretty(env)
                print('Model: minimize obj')
                load_model(env, obj)
                dump_model(env)
            except Exception as e:
                print(e)

