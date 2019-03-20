"""
bounds semantics unit-test.
"""

from wrapper import * # pylint: disable=unused-wildcard-import,wildcard-import

###
### DATA
###

OPTIONS = {
    "opt.priority"     : "box",
}

DECLS = {
    "bool" : (),                            # (name, ...)
    "int"  : (),                            # (name, ...)
    "rational" : ("x", "y", "z", "t"),      # (name, ...)
    "bv" : (),                              # ((name, width), ... )
    "fp" : ()                               # ((name, ebits, sbits), ... )
}

HARD = []

SOFT = {}

###
### BOUNDS SEMANTICS UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "x") as obj1, \
             create_minimize(env, "y", lower="(- 0.5)", upper="(/ 1 2)") as obj2, \
             create_minimize(env, "z", lower="0", upper="1") as obj3, \
             create_minimize(env, "t", lower="0", upper="0") as obj4, \
             create_maximize(env, "(+ y 1)") as obj5:
            assert_objective(env, obj1)
            assert_objective(env, obj2)
            assert_objective(env, obj3)
            assert_objective(env, obj4)
            assert_objective(env, obj5)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#     (x -oo)
#     (y -1/2)
#     (z 0)
#     (t unsat)
#     ((`+_rat` y 1) +oo)
# )
