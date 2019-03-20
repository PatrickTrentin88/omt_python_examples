"""
objective iterator and objective values unit-test.
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
    "bool" : (),                                    # (name, ...)
    "int"  : (),                                    # (name, ...)
    "rational" : ("a", "b", "c", "d", "eps", "oo"), # (name, ...)
    "bv" : (),                                      # ((name, width), ... )
    "fp" : ()                                       # ((name, ebits, sbits), ... )
}

HARD = [
    "(<= 42 a)",
    "(< b 3)",
]

SOFT = {}


###
### OBJITER UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        with create_minimize(env, "a") as obj1, \
             create_maximize(env, "b") as obj2, \
             create_minimize(env, "c") as obj3, \
             create_minimize(env, "d", lower="0", upper="0") as obj4:

            assert_objective(env, obj1)
            assert_objective(env, obj2)
            assert_objective(env, obj3)
            assert_objective(env, obj4)

            solve(env)

            print("\n\t### GET-OBJECTIVES ###")

            print("\n  -*- default approximation -*-")
            get_objectives(env)

            print("\n  -*- custom approximation -*-")
            INF = msat_from_string(env, "999999999999999999999")
            EPS = msat_from_string(env, "(/ 1 10000000000000000)")
            get_objectives(env, INF, EPS)

            print("\n  -*- symbolic with internal representation -*-")
            INF = msat_from_string(env, "oo")   # N.B.: already declared.
            EPS = msat_from_string(env, "eps")  # N.B.: already declared.
            get_objectives(env, INF, EPS)

            print("\n  -*- symbolic with pretty string -*-")
            get_objectives_pretty(env)

            print("\n\t### DUMP MODELS ###\n")
            dump_models(env)

            print("\n\t### DUMP OLD-STYLE STATS ###\n")
            dump_stats(env)

#
## EXPECTED OUTPUT
#
# sat
#
#   ### GET-OBJECTIVES ###
#
#   -*- default approximation -*-
# (objectives
#   (a 42)
#   (b 2999999/1000000)
#   (c -1000000000)
#   (d unsat)
# )
#
#   -*- custom approximation -*-
# (objectives
#   (a 42)
#   (b 29999999999999999/10000000000000000)
#   (c -999999999999999999999)
#   (d unsat)
# )
#
#   -*- symbolic with internal representation -*-
# (objectives
#   (a 42)
#   (b (`+_rat` 3 (`*_rat` -1 eps)))
#   (c (`*_rat` -1 oo))
#   (d unsat)
# )
#
#   -*- symbolic with pretty string -*-
# (objectives
#   (a 42)
#   (b (- 3 epsilon))
#   (c -oo)
#   (d unsat)
# )
#
#   ### DUMP MODELS ###
#
# % Goal: a
# % Status: MSAT_OPT_SAT_OPTIMAL
# % (Finite) Model:
#   a : 42
#   b : 0
#   c : 0
#   d : 1
#
# % Goal: b
# % Status: MSAT_OPT_SAT_OPTIMAL
# % (Finite) Model:
#   a : 42
#   b : 2999999/1000000
#   c : 0
#   d : 1
#
# % Goal: c
# % Status: MSAT_OPT_SAT_OPTIMAL
# % (Finite) Model:
#   a : 42
#   b : 2999999/1000000
#   c : -1000000000
#   d : 0
#
# % Goal: d
# % Status: MSAT_OPT_UNSAT
# % (Finite) Model:
#   no model available
#
#
#   ### DUMP OLD-STYLE STATS ###
#
# ### MINIMIZATION STATS ###
# # objective:      a
# # interval:     [ -INF, +INF ]
# #
# # Search terminated!
# # Exact non-strict optimum found!
# # Optimum: 42
# # Search steps: 2 (sat: 1)
# #  - binary: 0 (sat: 0)
# #  - linear: 2 (sat: 1)
# # Restarts: 3 [session: 3]
# # Decisions: 11 (0 random) [session: 11 (0 random)]
# # Propagations: 32 (0 theory) [session: 45 (0 theory)]
# # Watched clauses visited: 23 (4 binary) [session: 28 (9 binary)]
# # Conflicts: 3 (2 theory) [session: 3 (2 theory)]
# # Error:
# #  - absolute: 0
# #  - relative: +INF
# # Total time: 0.003 s
# #  - first solution: 0.000 s
# #  - optimization: 0.000 s
# #  - certification: 0.003 s
# # Memory used: 26.543 MB
#
# ### MAXIMIZATION STATS ###
# # objective:      b
# # interval:     [ -INF, +INF ]
# #
# # Search terminated!
# # Exact strict optimum found!
# # Optimum: <3
# # Search steps: 2 (sat: 1)
# #  - binary: 0 (sat: 0)
# #  - linear: 2 (sat: 1)
# # Restarts: 3 [session: 3]
# # Decisions: 11 (0 random) [session: 11 (0 random)]
# # Propagations: 32 (0 theory) [session: 45 (0 theory)]
# # Watched clauses visited: 23 (4 binary) [session: 28 (9 binary)]
# # Conflicts: 3 (2 theory) [session: 3 (2 theory)]
# # Error:
# #  - absolute: 0
# #  - relative: +INF
# # Total time: 0.003 s
# #  - first solution: 0.001 s
# #  - optimization: 0.000 s
# #  - certification: 0.002 s
# # Memory used: 26.543 MB
#
# ### MINIMIZATION STATS ###
# # objective:      c
# # interval:     [ -INF, +INF ]
# #
# # Search terminated!
# # Exact non-strict optimum found!
# # Optimum: -INF
# # Search steps: 1 (sat: 1)
# #  - binary: 0 (sat: 0)
# #  - linear: 1 (sat: 1)
# # Restarts: 2 [session: 2]
# # Decisions: 10 (0 random) [session: 10 (0 random)]
# # Propagations: 14 (0 theory) [session: 27 (0 theory)]
# # Watched clauses visited: 5 (2 binary) [session: 10 (7 binary)]
# # Conflicts: 0 (0 theory) [session: 0 (0 theory)]
# # Error:
# #  - absolute: 0
# #  - relative: +INF
# # Total time: 0.003 s
# #  - first solution: 0.002 s
# #  - optimization: 0.000 s
# #  - certification: 0.001 s
# # Memory used: 26.543 MB
#
# ### MINIMIZATION STATS ###
# # objective:      d
# # interval:     [ 0, 0 ]
# #
# # Search terminated!
# # No solution.
# # Search steps: 0 (sat: 0)
# #  - binary: 0 (sat: 0)
# #  - linear: 0 (sat: 0)
# # Restarts: 0 [session: 0]
# # Decisions: 0 (0 random) [session: 0 (0 random)]
# # Propagations: 0 (0 theory) [session: 0 (0 theory)]
# # Watched clauses visited: 0 (0 binary) [session: 0 (0 binary)]
# # Conflicts: 0 (0 theory) [session: 0 (0 theory)]
# # Error:
# #  - absolute: 0
# #  - relative: 0
# # Total time: 0.000 s
# #  - first solution: 0.000 s
# #  - optimization: 0.000 s
# #  - certification: 0.000 s
# # Memory used: 19.410 MB
#
