from input.input import gtw_pos, obj_pos, sta_pos, sta_cov, sta_link_distance
from input.input import sta_num
from input.input import gtw_lim, obj_lim, sta_lim
from solve.draw import draw_graph
from solve.network import Graph
from lin_prog.ilp_matrix import ILPMatrix
from lin_prog.milp_solver import solve_milp_problem
from lin_prog.lp_matrix import LPMatrix
from lin_prog.lp_solver import solve_lp_problem

import pandas as pd


G = Graph(gtw_pos, obj_pos, sta_pos,
          sta_cov, sta_link_distance)
G.create_graph()

draw_graph(G)


M = ILPMatrix(G, sta_num, gtw_lim, obj_lim, sta_lim)
M.create_matrix()
x = solve_milp_problem(M.f.values,
                       M.int_constraints,
                       M.ineq_array.values,
                       M.ineq_b,
                       M.eq_array.values,
                       M.eq_b,
                       M.lower_bounds,
                       M.upper_bounds)
solution = pd.Series(x, index=M.eq_array.columns.values)

# M = LPMatrix(G, sta_num, gtw_lim, obj_lim, sta_lim)
# M.create_matrix()
# res = solve_lp_problem(M.f.values,
#                        M.ineq_array.values,
#                        M.ineq_b,
#                        M.eq_array.values,
#                        M.eq_b,
#                        M.lower_bounds,
#                        M.upper_bounds)
#
# solution = pd.Series(res.x, index=M.eq_array.columns.values)
a = 1
