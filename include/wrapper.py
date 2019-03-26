"""
High level wrapper for OMT functionalities in the
mathsat library.
"""

import time
from contextlib import contextmanager
from mathsat import * # pylint: disable=unused-wildcard-import,wildcard-import

###
### Config Generator
###

@contextmanager
def create_config(cdict):
    """
    Create a new MathSAT configuration.

    :param cdict: a dictionary where the 'key' is the option name
                  and 'value' is the option value.

    :yields: a MathSAT configuration instance.
    """
    try:
        cfg = msat_create_config()
        assert not MSAT_ERROR_CONFIG(cfg)
        for key, value in cdict.items():
            if msat_set_option(cfg, key, value) != 0:
                raise Exception("Invalid key-value pair: <{}, {}>".format(key, value))
        yield cfg
    finally:
        if not MSAT_ERROR_CONFIG(cfg):
            msat_destroy_config(cfg)
    return

def destroy_config(cfg):
    """
    Destroys a MathSAT configuration.

    :param cfg: the MathSAT configuration instance to be destroyed.
    """
    assert not MSAT_ERROR_CONFIG(cfg)
    msat_destroy_config(cfg)
    return

###
### Environment Generator
###

@contextmanager
def create_env(cfg=None, other=None, optimizing=True):
    """
    Create a new MathSAT environment.

    :param cfg: the configuration to use.
    :param other: if present, the new MathSAT environment can share
                  terms with its sibling. It is an error to destroy
                  a new environment before its sibling.
    :param optimizing: enables the optimization capabilities on the
                       MathSAT environment.

    :yields: a MathSAT environment instance.
    """
    try:
        env = None
        if optimizing:
            env = msat_create_opt_env(cfg, other)
        else:
            env = msat_create_env(cfg, other)
        assert not MSAT_ERROR_ENV(env)
        yield env
    finally:
        if not MSAT_ERROR_ENV(env):
            msat_destroy_env(env)

def destroy_env(env):
    """
    Destroys a MathSAT environment.

    :param env: the MathSAT environment instance to be destroyed.
    """
    assert not MSAT_ERROR_ENV(env)
    msat_destroy_env(env)
    return

###
### OBJECTIVES
###

@contextmanager
def create_minimize(env, cost_fun, lower=None, upper=None, signed=False):
    """
    Create a new objective 'min(cost_fun)' with optional optimization
    local interval [lower, upper[.

    :param env: the environment in which to operate.
    :param cost_fun: the cost function to optimize.
    :param lower: a string representing the optimization lower bound.
    :param upper: a string representing the optimization upper bound.
    :param signed: when enabled, a Bit-Vector goal is interpreted as signed.

    :yields: a new msat_objective instance.
    """
    assert not MSAT_ERROR_ENV(env)
    try:
        tcf = string_to_term(env, cost_fun)
        lower_bound = string_to_term(env, lower) if lower is not None else None
        upper_bound = string_to_term(env, upper) if upper is not None else None
        obj = msat_make_minimize(env, tcf, lower_bound, upper_bound, signed)
        assert not MSAT_ERROR_OBJECTIVE(obj)
        yield obj
    finally:
        if 'obj' in locals() and not MSAT_ERROR_OBJECTIVE(obj):
            msat_destroy_objective(env, obj)
    return

@contextmanager
def create_maximize(env, cost_fun, lower=None, upper=None, signed=False):
    """
    Create a new objective 'max(cost_fun)' with optional optimization
    local interval ]lower, upper].

    :param env: the environment in which to operate.
    :param cost_fun: the cost function to optimize.
    :param lower: a string representing the optimization lower bound.
    :param upper: a string representing the optimization upper bound.
    :param signed: when enabled, a Bit-Vector goal is interpreted as signed.

    :yields: a new msat_objective instance.
    """
    assert not MSAT_ERROR_ENV(env)
    try:
        tcf = string_to_term(env, cost_fun)
        lower_bound = string_to_term(env, lower) if lower is not None else None
        upper_bound = string_to_term(env, upper) if upper is not None else None
        obj = msat_make_maximize(env, tcf, lower_bound, upper_bound, signed)
        assert not MSAT_ERROR_OBJECTIVE(obj)
        yield obj
    finally:
        if 'obj' in locals() and not MSAT_ERROR_OBJECTIVE(obj):
            msat_destroy_objective(env, obj)
    return

@contextmanager
def create_minmax(env, cost_funs, lower=None, upper=None, signed=False):
    """
    Create a new objective 'min(max(cost_fun[0]), ..., max(cost_fun[N]))'
    with optional optimization local interval ]lower, upper].

    :param env: the environment in which to operate.
    :param cost_funs: the cost functions to optimize.
    :param lower: a string representing the optimization lower bound.
    :param upper: a string representing the optimization upper bound.
    :param signed: when enabled, a Bit-Vector goal is interpreted as signed.

    :yields: a new msat_objective instance.
    """
    assert not MSAT_ERROR_ENV(env)
    try:
        tcfs = [string_to_term(env, cost_fun) for cost_fun in cost_funs]
        lower_bound = string_to_term(env, lower) if lower is not None else None
        upper_bound = string_to_term(env, upper) if upper is not None else None
        obj = msat_make_minmax(env, tcfs, lower_bound, upper_bound, signed)
        assert not MSAT_ERROR_OBJECTIVE(obj)
        yield obj
    finally:
        if 'obj' in locals() and not MSAT_ERROR_OBJECTIVE(obj):
            msat_destroy_objective(env, obj)
    return

@contextmanager
def create_maxmin(env, cost_funs, lower=None, upper=None, signed=False):
    """
    Create a new objective 'max(min(cost_fun[0]), ..., min(cost_fun[N]))'
    with optional optimization local interval [lower, upper[.

    :param env: the environment in which to operate.
    :param cost_funs: the cost functions to optimize.
    :param lower: a string representing the optimization lower bound.
    :param upper: a string representing the optimization upper bound.
    :param signed: when enabled, a Bit-Vector goal is interpreted as signed.

    :yields: a new msat_objective instance.
    """
    assert not MSAT_ERROR_ENV(env)
    try:
        tcfs = [string_to_term(env, cost_fun) for cost_fun in cost_funs]
        lower_bound = string_to_term(env, lower) if lower is not None else None
        upper_bound = string_to_term(env, upper) if upper is not None else None
        obj = msat_make_maxmin(env, tcfs, lower_bound, upper_bound, signed)
        assert not MSAT_ERROR_OBJECTIVE(obj)
        yield obj
    finally:
        if 'obj' in locals() and not MSAT_ERROR_OBJECTIVE(obj):
            msat_destroy_objective(env, obj)
    return

def destroy_obj(env, obj):
    """
    Destroys a msat_objective instance.

    :param env: the environment in which to operate.
    :param obj: the msat_objective instance to be destroyed.
    """
    assert not MSAT_ERROR_ENV(env)
    assert not MSAT_ERROR_OBJECTIVE(obj)
    msat_destroy_objective(env, obj)
    return

###
### Formula/Objective Stack
###

def push(env):
    """
    Pushes a checkpoint for backtracking in an environment.

    :param env: the environment in which to operate.
    """
    assert not MSAT_ERROR_ENV(env)
    if msat_push_backtrack_point(env) != 0:
        raise Exception("Error while pushing a backtrack point.")
    return

def pop(env):
    """
    Backtracks to the last checkpoint set in the environment.

    :param env: the environment in which to operate.
    """
    assert not MSAT_ERROR_ENV(env)
    if msat_pop_backtrack_point(env) != 0:
        raise Exception("Error while popping a backtrack point.")
    return

def string_to_term(env, srepr):
    """
    Creates a term from its string representation.

    The syntax of 'repr' is that of the SMT-LIBv2. All the
    variables and functions must have been previously declared
    in 'env'.

    :param env: the environment of the definition.
    :param srepr: the string to parse, in SMT-LIBv2 format.

    :returns: the created term.
    """
    assert not MSAT_ERROR_ENV(env)
    term = msat_from_string(env, srepr)
    if MSAT_ERROR_TERM(term):
        raise Exception("Unable to convert '{}' to msat_term.".format(str(srepr)))
    return term

def assert_string_formula(env, hard):
    """
    Adds a logical formula to an environment.

    :param env: the environment in which the formula is asserted.
    :param hard: the string representation of the formula to
                 be asserted.
    """
    assert not MSAT_ERROR_ENV(env)
    tcons = string_to_term(env, hard)
    if msat_assert_formula(env, tcons) != 0:
        raise Exception("Unable to assert formula '{}'.".format(str(hard)))
    return

def assert_string_formulas(env, hard_list):
    """
    Adds a logical formula to an environment.

    :param env: the environment in which the formulas are asserted.
    :param hard_list: a list of strings representing the formulas to
                      be asserted.
    """
    for hard_cons in hard_list:
        assert_string_formula(env, hard_cons)
    return

def assert_string_soft_formula(env, sid, soft):
    """
    Adds a logical soft-constraint formula to an environment.

    :param env: the environment in which the soft-formula is asserted.
    :param sid: the identifier of the group of soft-formulas to
                which it belongs.
    :param soft: the string representation of the soft-formula to
                 be asserted.
    """
    assert not MSAT_ERROR_ENV(env)
    tcons = string_to_term(env, soft[0])
    weight = string_to_term(env, soft[1])
    msat_assert_soft_formula(env, tcons, weight, sid)
    return

def assert_string_soft_formulas_list(env, sid, slist): # pylint: disable=invalid-name,locally-disabled
    """
    Adds a list of logical soft-constraint formulas to an environment.

    :param env: the environment in which the soft-formulas are asserted.
    :param sid: the identifier of the group of soft-formulas.
    :param slist: a list of strings representing the soft-formulas to
                 be asserted.
    """
    for soft in slist:
        assert_string_soft_formula(env, sid, soft)
    return

def assert_string_soft_formulas_dict(env, sdict): # pylint: disable=invalid-name,locally-disabled
    """
    Adds a set of logical soft-constraint formulas to an environment.

    :param env: the environment in which the soft-formulas are asserted.
    :param sdict: a dictionary where 'key' is the identifier of a group
                  of soft-formula and 'value' is a list of strings
                  representing the soft-formulas contained in such group.
    """
    for sid, slist in sdict.items():
        assert_string_soft_formulas_list(env, sid, slist)
    return

def assert_objective(env, obj):
    """
    Adds an objective to an environment, so that it will be
    optimized at the next msat_solve().

    :param env: the environment in which to operate.
    :param obj: the msat_objective instance to be asserted.
    """
    assert not MSAT_ERROR_ENV(env)
    assert not MSAT_ERROR_OBJECTIVE(obj)
    if msat_assert_objective(env, obj) != 0:
        raise Exception("Unable to assert objective function.")
    return

###
### DECLARE VARIABLES
###

def make_var(env, name, vtp):
    """
    Declares a variable with identifier 'name'
    and type 'vtp' in the given environment.

    :param env: the environment in which to operate.
    :param name: the name of the variable.
    :param vtp: the variable type.

    :returns: a msat_term variable.
    """
    assert not MSAT_ERROR_ENV(env)
    assert not MSAT_ERROR_TYPE(vtp)
    decl = msat_declare_function(env, name, vtp)
    assert not MSAT_ERROR_DECL(decl)
    term = msat_make_constant(env, decl)
    assert not MSAT_ERROR_TERM(term)
    return term

def make_bool_var(env, name):
    """
    Declares a variable with identifier 'name'
    and Boolean type in the given environment.

    :param env: the environment in which to operate.
    :param name: the name of the variable.

    :returns: a msat_term variable.
    """
    assert not MSAT_ERROR_ENV(env)
    vtp = msat_get_bool_type(env)
    return make_var(env, name, vtp)

def make_int_var(env, name):
    """
    Declares a variable with identifier 'name'
    and Integer type in the given environment.

    :param env: the environment in which to operate.
    :param name: the name of the variable.

    :returns: a msat_term variable.
    """
    assert not MSAT_ERROR_ENV(env)
    vtp = msat_get_integer_type(env)
    return make_var(env, name, vtp)

def make_rational_var(env, name):
    """
    Declares a variable with identifier 'name'
    and Rational type in the given environment.

    :param env: the environment in which to operate.
    :param name: the name of the variable.

    :returns: a msat_term variable.
    """
    assert not MSAT_ERROR_ENV(env)
    vtp = msat_get_rational_type(env)
    return make_var(env, name, vtp)

def make_bv_var(env, name, width):
    """
    Declares a variable with identifier 'name'
    and Bit-Vector type in the given environment.

    :param env: the environment in which to operate.
    :param name: the name of the variable.
    :param width: the Bit-Vector width.

    :returns: a msat_term variable.
    """
    assert not MSAT_ERROR_ENV(env)
    vtp = msat_get_bv_type(env, width)
    return make_var(env, name, vtp)

def make_fp_var(env, name, ebits, sbits):
    """
    Declares a variable with identifier 'name'
    and Floating-Point type in the given environment.

    :param env: the environment in which to operate.
    :param name: the name of the variable.
    :param ebits: the number of bits in the exponent.
    :param sbits: the number of bits in the significand/mantissa.

    :returns: a msat_term variable.
    """
    assert not MSAT_ERROR_ENV(env)
    vtp = msat_get_fp_type(env, ebits, sbits)
    return make_var(env, name, vtp)

def make_bool_vars(env, nlist):
    """
    Declares a list of Boolean variables.

    :param env: the environment in which to operate.
    :param nlist: the list of variable names.

    :returns: the list of msat_term variables declared.
    """
    return [make_bool_var(env, name) for name in nlist]

def make_int_vars(env, nlist):
    """
    Declares a list of Integer variables.

    :param env: the environment in which to operate.
    :param nlist: the list of variable names.

    :returns: the list of msat_term variables declared.
    """
    return [make_int_var(env, name) for name in nlist]

def make_rational_vars(env, nlist):
    """
    Declares a list of Rational variables.

    :param env: the environment in which to operate.
    :param nlist: the list of variable names.

    :returns: the list of msat_term variables declared.
    """
    return [make_rational_var(env, name) for name in nlist]

def make_bv_vars(env, nlist):
    """
    Declares a list of Bit-Vector variables.

    :param env: the environment in which to operate.
    :param nlist: a list of '(name, width)' pairs.

    :returns: the list of msat_term variables declared.
    """
    return [make_bv_var(env, name, width) for name, width in nlist]

def make_fp_vars(env, nlist):
    """
    Declares a list of Floating-Point variables.

    :param env: the environment in which to operate.
    :param nlist: a list of '(name, ebits, sbits)' triplets.

    :returns: the list of msat_term variables declared.
    """
    return [make_fp_var(env, name, ebits, sbits) for name, ebits, sbits in nlist]

def make_all_vars(env, vdict):
    """
    Declares Boolean, Integer, Rational, Bit-Vector and
    Floating-Point variables in the given dictionary.

    :param env: the environment in which to operate.
    :param vdict: a dictionary where 'key' is the variable type
                  (supported: bool|int|rational|bv|fp) and 'value'
                  is the corresponding list of variable names and
                  additional data required to declare the variables.
    :returns: a dictionary where 'key' is the variable type
              and 'value' is the list of msat_term variables
              of such type.
    """
    ret = {}
    for vtype, nlist in vdict.items():
        if vtype == "bool":
            ret["bool"] = make_bool_vars(env, nlist)
        elif vtype == "int":
            ret["int"] = make_int_vars(env, nlist)
        elif vtype == "rational":
            ret["rational"] = make_rational_vars(env, nlist)
        elif vtype == "bv":
            ret["bv"] = make_bv_vars(env, nlist)
        elif vtype == "fp":
            ret["fp"] = make_fp_vars(env, nlist)
        else:
            raise Exception("Unsupported type '{}'.".format(vtype))
    return ret

###
### SOLVE / SOLVE ALL
###

def solve(env):
    """
    Checks the satisfiability of the given environment.

    :param env: the environment to check.

    :returns:
        MSAT_SAT if the problem is satisfiable
        MSAT_UNSAT if it is unsatisfiable, and
        MSAT_UNKNOWN if there was some error or if the
                     satisfiability can't be determined.
    """
    ret = msat_solve(env)
    if ret > 0:
        print("sat")
    elif ret < 0:
        print("unknown")
    else:
        print("unsat")
    return ret

def solve_all_sat(env, important):
    """
    Performs AllSat over the important atoms of the conjunction
    of all formulas asserted in the given environment. When used
    in incremental mode, a backtrack-point should be pushed before
    calling this function, and popped after this call has completed.
    Not doing this changes the satisfiability of the formula.

    :param env: the environment to check.
    :param important: an array of important atoms.

    :returns: an over-approximation of the number of models found,
        or -1 on error. If the solver detects that the formula is a
        tautology, -2 is returned.
    """
    callback = AllSatModelPrinter(env)
    important = [string_to_term(env, el) for el in important]
    ret = msat_all_sat(env, important, callback)
    if ret == -2:
        print("tautology")
    elif ret == -1:
        print("unknown")
    elif ret == 0:
        print("unsat")
    return ret

###
### ALL-SAT MODEL PRINTER
###

class AllSatModelPrinter(object): # pylint: disable=too-few-public-methods,locally-disabled
    """
    A simple class for printing models found by the all_sat() procedure.
    """

    def __init__(self, env):
        """
        Class constructor.

        :param env: the environment in which to operate.
        """
        self._env = env
        self._first = True

    def __call__(self, data):
        """
        Callback function, invocked each time a model is found.

        :param data: the model-assignment over the important
                     atoms of the all_sat() search.
        :returns: 1 to continue the search.
        """
        if self._first:
            print("sat")
            self._first = False
            get_objectives_pretty(self._env)
        print("sat")
        for term in data:
            value = "True"
            if msat_term_is_not(self._env, term):
                term = msat_make_not(self._env, term)
                value = "False"
            print("\t{} : {}".format(str(term), str(value)))
        return 1

###
### GET_OBJECTIVES
###

def get_objectives(env, inf=None, eps=None):
    """
    Prints the list of objectives currently asserted
    and their value.

    :param env: the environment in which to operate.
    :param inf: the symbolic/constant value representing
                an infinite amount.
    :param eps: the symbolic/constant value representing
                an infinitesimal amount.
    """
    obj_iter = msat_create_objective_iterator(env)
    assert not MSAT_ERROR_OBJECTIVE_ITERATOR(obj_iter)
    print("(objectives")
    while msat_objective_iterator_has_next(obj_iter):
        res, obj = msat_objective_iterator_next(obj_iter)
        assert res == 0
        cost_fun = msat_objective_get_term(env, obj)
        assert not MSAT_ERROR_TERM(cost_fun)

        res = msat_objective_result(env, obj)
        if res < 0:
            print("\t({} unknown)".format(str(cost_fun)))
        elif res == 0:
            print("\t({} unsat)".format(str(cost_fun)))
        else:
            value = msat_objective_value_term(env, obj, MSAT_OPTIMUM,
                                              inf, eps)
            assert not MSAT_ERROR_TERM(value)
            print("\t({} {})".format(str(cost_fun), str(value)))
    print(")")
    msat_destroy_objective_iterator(obj_iter)

def get_objectives_pretty(env):
    """
    Prints the list of objectives currently asserted
    and their value, in a pretty format.

    :param env: the environment in which to operate.
    """
    obj_iter = msat_create_objective_iterator(env)
    assert not MSAT_ERROR_OBJECTIVE_ITERATOR(obj_iter)
    print("(objectives")
    while msat_objective_iterator_has_next(obj_iter):
        res, obj = msat_objective_iterator_next(obj_iter)
        assert res == 0
        cost_fun = msat_objective_get_term(env, obj)
        assert not MSAT_ERROR_TERM(cost_fun)
        value = get_objective_value_pretty_string(env, obj, MSAT_OPTIMUM)
        print("\t({} {})".format(str(cost_fun), value))
    print(")")
    msat_destroy_objective_iterator(obj_iter)

def get_objective_value_pretty_string(env, obj, val): # pylint: disable=invalid-name,locally-disabled
    """
    Returns a pretty string representing the given
    objective value.

    :param env: the environment in which to operate.
    :param obj: the msat_objective instance of reference.
    :param val: the objective value to evaluate.

    :returns: a string representing the target objective
              value.
    """
    ret = ""
    res = msat_objective_result(env, obj)
    if val == MSAT_OPTIMUM and res <= 0:
        if res == MSAT_UNKNOWN:
            ret = "unknown"
        elif res == MSAT_UNSAT:
            ret = "unsat"
    else:
        if msat_objective_value_is_minus_inf(env, obj, val) > 0:
            ret = "-oo"
        elif msat_objective_value_is_plus_inf(env, obj, val) > 0:
            ret = "+oo"
        else:
            term = msat_objective_value_term(env, obj, val,
                                             MSAT_MAKE_ERROR_TERM(),
                                             msat_from_string(env, "0"))

            eps = msat_objective_value_get_epsilon(env, obj, val)

            if eps > 0:
                ret = "(+ {} epsilon)".format(term)
            elif eps < 0:
                ret = "(- {} epsilon)".format(term)
            else:
                ret = str(term)
    return ret

###
### MODEL(s)
###

def load_model(env, obj):
    """
    Loads the model associated with an objective instance 'obj'
    within the environment (if any).

    :param env: the environment in which to operate.
    :param obj: the target objective.
    """
    msat_load_objective_model(env, obj)

def dump_models(env):
    """
    Prints the model associated with each objective currently
    asserted in the given environment.

    :param env: the environment in which to operate.
    """
    svector = ["MSAT_OPT_UNKNOWN",
               "MSAT_OPT_UNSAT",
               "MSAT_OPT_SAT_PARTIAL",
               "MSAT_OPT_SAT_APPROX",
               "MSAT_OPT_SAT_OPTIMAL"]
    obj_iter = msat_create_objective_iterator(env)
    assert not MSAT_ERROR_OBJECTIVE_ITERATOR(obj_iter)
    while msat_objective_iterator_has_next(obj_iter):
        res, obj = msat_objective_iterator_next(obj_iter)
        assert res == 0
        cost_fun = msat_objective_get_term(env, obj)
        assert not MSAT_ERROR_TERM(cost_fun)
        status = msat_objective_result(env, obj)
        print("% Goal: {}".format(str(cost_fun)))
        print("% Status: {}".format(svector[status+1]))
        print("% (Finite) Model:")
        if status > 0:
            load_model(env, obj)
            dump_model(env)
        else:
            print("\tno model available")
        print("")
    msat_destroy_objective_iterator(obj_iter)

def dump_model(env, hidden=False):
    """
    Prints the model currently loaded in the given
    environment.

    :param env: the environment in which to operate.
    :param hidden: enables printing the value of hidden
                   variables.
    """
    model = msat_get_model(env)
    if MSAT_ERROR_MODEL(model):
        raise Exception("Unable to get model from environment.")
    assert not MSAT_ERROR_MODEL(model)
    miter = msat_model_create_iterator(model)
    assert not MSAT_ERROR_MODEL_ITERATOR(miter)
    while msat_model_iterator_has_next(miter):
        (term, value) = msat_model_iterator_next(miter)
        if str(term)[0] == "." and not hidden:
            continue
        else:
            print("\t{} : {}".format(str(term), str(value)))
    msat_destroy_model_iterator(miter)
    msat_destroy_model(model)

###
### OLD-STYLE STAT(s)
###

def dump_stats(env):
    """
    Prints the optimization statistics for each
    objective currently asserted in the given
    environment.

    :param env: the environment in which to operate.
    """
    obj_iter = msat_create_objective_iterator(env)
    assert not MSAT_ERROR_OBJECTIVE_ITERATOR(obj_iter)
    while msat_objective_iterator_has_next(obj_iter):
        res, obj = msat_objective_iterator_next(obj_iter)
        assert res == 0
        stats = msat_objective_get_search_stats(env, obj)
        print(stats)
    msat_destroy_objective_iterator(obj_iter)

###
### Timer() -- sets a search timeout
###

class Timer(object): # pylint: disable=too-few-public-methods,locally-disabled
    """A simple timer object."""

    def __init__(self, timeout):
        """
        Timer Constructor.

        :param timeout: the number of seconds before a timeout.
        """
        self._timeout = timeout
        self._started = False
        self._start = 0.0
        self._end = 0.0

    def __call__(self):
        """
        Callback function.

        :returns: non-zero upon timeout.
        """
        now = time.time()
        if not self._started:
            self._started = now
        self._end = now
        ret = 0
        if self._end - self._started > self._timeout:
            ret = 1
        return ret

    def reset(self):
        """
        Reset the timer.
        """
        self._started = False
        return

###
###
###

if __name__ == "__main__":
    pass
