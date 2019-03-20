"""
incremental OMT unit-test.
"""

from wrapper import * # pylint: disable=unused-wildcard-import,wildcard-import

###
### DATA
###

OPTIONS = {}

DECLS = {
    "bool" : (),        # (name, ...)
    "int"  : (),        # (name, ...)
    "rational" : ("x"), # (name, ...)
    "bv" : (),          # ((name, width), ... )
    "fp" : (),          # ((name, ebits, sbits), ... )
}

HARD = []

SOFT = {}

###
### INCREMENTAL UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)

        with create_minimize(env, "x") as obj:

            push(env)
            assert_objective(env, obj)
            assert_string_formula(env, "(<= 5 x)")
            solve(env)
            get_objectives_pretty(env)
            pop(env)

            push(env)
            assert_objective(env, obj)
            solve(env)
            get_objectives_pretty(env)
            pop(env)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (x 5)
# )
# sat
# (objectives
#   (x -oo)
# )
# sat
# (objectives
# )
