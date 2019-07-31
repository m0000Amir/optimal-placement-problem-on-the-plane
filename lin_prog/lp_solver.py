"""
Minimizing  objective function of linear programing problem using the
simplex algorithm
"""
from scipy.optimize import linprog
import numpy as np


def solve_lp_problem(obj_func, ineq_array, ineq_b, eq_array, eq_b, lb, ub):

    b_array = np.vstack([lb, ub])
    minmax_bounds = tuple((b_array[0, i], b_array[1, i])
                          for i in range(len(b_array[0])))

    res = linprog(obj_func, A_ub=ineq_array, b_ub=ineq_b,
                  A_eq=eq_array, b_eq=eq_b, bounds=minmax_bounds,
                  method='simplex', callback=None,
                  options={'disp': True})
    assert round(res.fun) == 0, ('There is no solution because the '
                                 'objective function value of linear '
                                 'programing problem is not zero')
    return res
