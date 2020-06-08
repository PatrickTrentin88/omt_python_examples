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

# pylint:disable=import-error, wrong-import-position
from wrapper import create_config, create_env, msat_set_termination_test, \
                    msat_from_smtlib2, MSAT_ERROR_TERM, msat_assert_formula, \
                    Timer, string_to_term, msat_make_minimize, \
                    assert_objective, solve, get_objectives_pretty, \
                    load_model, dump_model  # noqa: E402

###############################################################################
###############################################################################
###############################################################################

# DATA

OPTIONS = {
    "model_generation": "true",
    "opt.soft_timeout": "false",
    "opt.verbose": "true",
    "opt.maxsmt_engine": "omt",  # Possible values: omt, maxres
    "opt.priority": "lex",  # Possible values: box, lex
}

#filename: str = os.path.join(BASE_DIR, 'smt2-files', 'Mz2-noAbs',
filename: str = os.path.join(BASE_DIR, 'examples',
                             'A012-dzn-fzn_v3.smt2')

# PROGRAM

with create_config(OPTIONS) as cfg:
    with create_env(cfg, optimizing=True) as env:
        with open(filename, 'r') as f:
            FORMULA = msat_from_smtlib2(env, f.read())
            if MSAT_ERROR_TERM(FORMULA):
                print(f'''Unable to parse {filename}''')
            msat_assert_formula(env, FORMULA)

            # Set a timeout
            CALLBACK = Timer(300.0)
            msat_set_termination_test(env, CALLBACK)

            signed: bool = True

            try:
                TCF = string_to_term(env, 'obj')
                # TODO: Any way to add lower und upper bounds?
                OBJ = msat_make_minimize(env, TCF, signed)
                assert_objective(env, OBJ)
                solve(env)
                get_objectives_pretty(env)
                print('Model: minimize objective')
                load_model(env, OBJ)
                dump_model(env)
            # TODO: pylint:disable=broad-except
            except Exception as exception:
                print(f'''Exception raised: {exception}''')
