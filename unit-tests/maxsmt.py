"""
MaxSMT unit-test.
"""

from wrapper import * # pylint: disable=unused-wildcard-import,wildcard-import

###
### DATA
###

OPTIONS = {
    "opt.maxsmt_engine" : "maxres",
    "model_generation"  : "true",
}

DECLS = {
    "bool" : (),            # (name, ...)
    "int"  : ("x", "y"),    # (name, ...)
    "rational" : (),        # (name, ...)
    "bv" : (),              # ((name, width), ... )
    "fp" : ()               # ((name, ebits, sbits), ... )
}

HARD = [
    "(= x (- y))"
]

SOFT = {
    "goal" : (
        ("(< x 0)", "1"),
        ("(< x y)", "1"),
        ("(< y 0)", "1")
    )
}

###
### MAXSMT UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "goal", upper="2") as obj:

            assert_objective(env, obj)
            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (goal 1)
# )
