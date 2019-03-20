"""
Pareto OMT unit-test.
"""

from wrapper import * # pylint: disable=unused-wildcard-import,wildcard-import

###
### DATA
###

OPTIONS = {
    "model_generation" : "true",
    "opt.priority"     : "par",
    "opt.par.mode"     : "incremental"
}

DECLS = {
    "bool" : (),                # (name, ...)
    "int"  : (),                # (name, ...)
    "rational" : ("a", "b"),    # (name, ...)
    "bv" : (),                  # ((name, width), ... )
    "fp" : ()                   # ((name, ebits, sbits), ... )
}

HARD = [
    """(or
        (and (= a 1) (= b 1))
        (and (= a 2) (= b 1))
        (and (= a 1) (= b 2))
        (and (= a 2) (= b 2))
        (and (= a 3) (= b 1))
        (and (= a 1) (= b 3))
    )"""
]

SOFT = {}

###
### PARETO UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_maximize(env, "a") as obj1, \
             create_maximize(env, "b") as obj2:
            assert_objective(env, obj1)
            assert_objective(env, obj2)

            while solve(env) > 0:
                dump_model(env)

#
## EXPECTED OUTPUT
#
# sat
#   a : 3
#   b : 1
# sat
#   a : 1
#   b : 3
# sat
#   a : 2
#   b : 2
# unsat
