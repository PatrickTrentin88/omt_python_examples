"""
Multi-Independent optimization unit-test.
"""

from wrapper import * # pylint: disable=unused-wildcard-import,wildcard-import

###
### DATA
###

OPTIONS = {
    "opt.priority"     : "box",
}

DECLS = {
    "bool" : (),                    # (name, ...)
    "int"  : (),                    # (name, ...)
    "rational" : ("x", "y", "z"),   # (name, ...)
    "bv" : (),                      # ((name, width), ... )
    "fp" : ()                       # ((name, ebits, sbits), ... )
}

HARD = ["(<= 42 x)", "(<= y x)"]

SOFT = {}

###
### BOXED UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "x") as obj1, \
             create_maximize(env, "y") as obj2, \
             create_maximize(env, "z", upper="50") as obj3:

            assert_objective(env, obj1)
            assert_objective(env, obj2)
            assert_objective(env, obj3)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (x 42)
#   (y +oo)
#   (z 50)
# )
