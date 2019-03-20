"""
objective combination unit-test.
"""

from wrapper import * # pylint: disable=unused-wildcard-import,wildcard-import

###
### DATA
###

OPTIONS = {
    "opt.priority"     : "box",
    "model_generation" : "true",
}

DECLS = {
    "bool" : ("m0", "m1", "m2", "m3"),              # (name, ...)
    "int"  : (),                                    # (name, ...)
    "rational" : ("q0", "q1", "q2", "q3",
                  "production_cost", "total_cost"), # (name, ...)
    "bv" : (("y", 4), ),                            # ((name, width), ... )
    "fp" : (("z", 2, 4), )                          # ((name, ebits, sbits), ... )
}

HARD = [
    # set goods quantity
    "(<= 1100 (+ q0 q1 q2 q3))",
    # set goods produced per machine
    "(and (<= 0 q0) (<= q0 800))",
    "(and (<= 0 q1) (<= q1 500))",
    "(and (<= 0 q2) (<= q2 600))",
    "(and (<= 0 q3) (<= q3 200))",
    # set machine `used` flag
    "(=> (< 0 q0) m0)",
    "(=> (< 0 q1) m1)",
    "(=> (< 0 q2) m2)",
    "(=> (< 0 q3) m3)",
    # def goals
    "(= production_cost (+ (* q0 8) (* q1 9) (* q2 9) (* q3 5)))"
]

SOFT = {
    "used_machines" : (
        ("(not m0)", "1"),
        ("(not m1)", "1"),
        ("(not m2)", "1"),
        ("(not m3)", "1"),
    )
}

###
### COMBINATION UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        assert_string_formula(env, \
        "(= total_cost (+ production_cost (* (/ 785 10) (+ (* 2 used_machines) 8))))")

        with create_minimize(env, "production_cost") as production_cost, \
             create_minimize(env, "total_cost") as total_cost:

            assert_objective(env, production_cost)
            assert_objective(env, total_cost)

            solve(env)
            get_objectives_pretty(env)

            print("\nModel: production_cost")
            load_model(env, production_cost)
            dump_model(env)

            print("\nModel: total_cost")
            load_model(env, total_cost)
            dump_model(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (production_cost 8300)
#   (total_cost 9399)
# )
#
# Model: production_cost
#   m0 : `true`
#   m1 : `true`
#   m2 : `true`
#   m3 : `true`
#   q0 : 800
#   q1 : 1/2000000
#   q2 : 199999999/2000000
#   q3 : 200
#   production_cost : 8300
#   total_cost : 9556
#   used_machines : 4
#
# Model: total_cost
#   m0 : `true`
#   m1 : `true`
#   m2 : `false`
#   m3 : `true`
#   q0 : 800
#   q1 : 100
#   q2 : 0
#   q3 : 200
#   production_cost : 8300
#   total_cost : 9399
#   used_machines : 3
