"""
bounds syntax unit-test.
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
    "bool" : (),            # (name, ...)
    "int"  : (),            # (name, ...)
    "rational" : ("x"),     # (name, ...)
    "bv" : (("y", 4), ),    # ((name, width), ... )
    "fp" : (("z", 2, 4), )  # ((name, ebits, sbits), ... )
}

HARD = []

SOFT = {}

INT_BOUND = "14"
REAL_BOUND = "(/ 5 2)"
BV_BOUND = "#b1001"
FP_BOUND = "(fp #b0 #b01 #b0100)"

###
### BOUNDS SYNTAX UNIT-TEST
###

with create_config(OPTIONS) as cfg:
    with create_env(cfg) as env:

        make_all_vars(env, DECLS)
        assert_string_formulas(env, HARD)
        assert_string_soft_formulas_dict(env, SOFT)

        # LIRA OBJECTIVES

        push(env)

        with create_minimize(env, "x") as unbounded_x, \
             create_minimize(env, "x", lower="(+ 5 (/ 3 2))") as min_sum_x, \
             create_minimize(env, "x", lower=INT_BOUND) as min_int_x, \
             create_maximize(env, "x", upper=INT_BOUND) as max_int_x, \
             create_minimize(env, "x", lower=REAL_BOUND) as min_real_x, \
             create_maximize(env, "x", upper=REAL_BOUND) as max_real_x, \
             create_minimize(env, "x", lower="(- (/ 21 7))", upper="(/ 21 7)") as min_const_x, \
             create_maximize(env, "x", lower="(- (/ 21 8))", upper="3") as max_const_x, \
             create_minimize(env, "x", lower="10", upper="1") as unsat_1_x, \
             create_minimize(env, "x", lower="10", upper="10") as unsat_2_x:

            assert_objective(env, unbounded_x)
            assert_objective(env, min_sum_x)
            assert_objective(env, min_int_x)
            assert_objective(env, max_int_x)
            assert_objective(env, min_real_x)
            assert_objective(env, max_real_x)
            assert_objective(env, min_const_x)
            assert_objective(env, max_const_x)
            assert_objective(env, unsat_1_x)
            assert_objective(env, unsat_2_x)

            solve(env)
            get_objectives_pretty(env)

        pop(env)

        # BV OBJECTIVES

        push(env)

        with create_minimize(env, "y") as unbounded_y, \
             create_minimize(env, "y", lower=BV_BOUND) as min_ubv_y, \
             create_maximize(env, "y", upper=BV_BOUND) as max_ubv_y, \
             create_minimize(env, "y", lower=BV_BOUND) as min_sbv_y, \
             create_maximize(env, "y", upper=BV_BOUND) as max_sbv_y, \
             create_minimize(env, "y", lower="((_ to_bv 4) 0)",
                             upper="((_ to_bv 4) 5)") as min_const_ubv_y, \
             create_maximize(env, "y", lower="#b0000",
                             upper="((_ to_bv 4) 5)") as max_const_ubv_y, \
             create_minimize(env, "y", lower="((_ to_bv 4) (- 5))",
                             upper="((_ to_bv 4) 5)",
                             signed=True) as min_const_sbv_y, \
             create_maximize(env, "y", lower="((_ to_bv 4) (- 5))",
                             upper="((_ to_bv 4) 5)",
                             signed=True) as max_const_sbv_y, \
             create_minimize(env, "y", lower="((_ to_bv 4) (- 5))",
                             upper="((_ to_bv 4) 5)") as unsat_1_y, \
             create_minimize(env, "y", lower="#b0111", upper="#b0001") as unsat_2_y, \
             create_minimize(env, "y", lower="#b0111", upper="#b0111") as unsat_3_y, \
             create_minimize(env, "y", lower="#b0000", upper="#b1111", signed=True) as unsat_4_y:

            assert_objective(env, unbounded_y)
            assert_objective(env, min_ubv_y)
            assert_objective(env, max_ubv_y)
            assert_objective(env, min_sbv_y)
            assert_objective(env, max_sbv_y)
            assert_objective(env, min_const_ubv_y)
            assert_objective(env, max_const_ubv_y)
            assert_objective(env, min_const_sbv_y)
            assert_objective(env, max_const_sbv_y)
            assert_objective(env, unsat_1_y)
            assert_objective(env, unsat_2_y)
            assert_objective(env, unsat_3_y)
            assert_objective(env, unsat_4_y)

            solve(env)
            get_objectives_pretty(env)

        pop(env)

        # FP OBJECTIVES

        push(env)

        with create_minimize(env, "z") as unbounded_z, \
             create_minimize(env, "z", lower=FP_BOUND) as min_fp_z, \
             create_maximize(env, "z", upper=FP_BOUND) as max_fp_z, \
             create_minimize(env, "z", lower="((_ to_fp 2 5) RNE (- 0.2))",
                             upper="(fp #b0 #b10 #b0000)") as min_const_fp_z, \
             create_maximize(env, "z", lower="((_ to_fp 2 5) RNE (- (/ 1 5)))",
                             upper="((_ to_fp 2 5) RNE 1.45)") as max_const_fp_z, \
             create_minimize(env, "z", lower="((_ to_fp 2 5) RNE 2)",
                             upper="((_ to_fp 2 5) RNE 1)") as unsat_1_z, \
             create_minimize(env, "z", lower="((_ to_fp 2 5) RNE 2)",
                             upper="((_ to_fp 2 5) RNE 2)") as unsat_2_z:
            assert_objective(env, unbounded_z)
            assert_objective(env, min_fp_z)
            assert_objective(env, max_fp_z)
            assert_objective(env, min_const_fp_z)
            assert_objective(env, max_const_fp_z)
            assert_objective(env, unsat_1_z)
            assert_objective(env, unsat_2_z)

            solve(env)
            get_objectives_pretty(env)

        pop(env)

#
## EXPECTED OUTPUT
#
# sat
# (objectives
#   (x -oo)
#   (x 13/2)
#   (x 14)
#   (x 14)
#   (x 5/2)
#   (x 5/2)
#   (x -3)
#   (x 3)
#   (x unsat)
#   (x unsat)
# )
# sat
# (objectives
#   (y 0_4)
#   (y 9_4)
#   (y 9_4)
#   (y 9_4)
#   (y 9_4)
#   (y 0_4)
#   (y 5_4)
#   (y 11_4)
#   (y 5_4)
#   (y unsat)
#   (y unsat)
#   (y unsat)
#   (y unsat)
# )
# sat
# (objectives
#   (z -oo)
#   (z 20_2_4)
#   (z 20_2_4)
#   (z 67_2_4)
#   (z 23_2_4)
#   (z unsat)
#   (z unsat)
# )
