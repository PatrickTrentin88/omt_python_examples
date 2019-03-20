"""
assert-soft unit-test.
"""

from wrapper import * # pylint: disable=unused-wildcard-import,wildcard-import

###
### DATA
###

OPTIONS = {
    "opt.priority" : "box"
}

HARD = []

SOFT = {
    "goal" : (
        ("false", "1"),
        ("false", "0"),
        ("false", "5"),
        ("false", "0.5"),
        ("false", "(+ 3 (/ 4 2))"),
        ("false", "(/ 2 4)"),
        ("false", "(- 16)"),
        ("false", "(- (/ 2 4))"),
        ("false", "(- 0.5)"),
    )
}

###
### ASSERT-SOFT UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "goal") as obj:
            assert_objective(env, obj)

            solve(env)
            get_objectives_pretty(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#     (goal -5)
# )
