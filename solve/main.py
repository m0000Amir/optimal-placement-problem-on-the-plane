from input.input import gtw_pos, obj_pos, sta_pos
from input.input import coverage, link_distance
from input.input import gtw_lim, obj_lim, sta_lim
from input.input import problem


from solve.network import Graph
from lin_prog.ilp_matrix import ILPMatrix
from lin_prog.milp_solver import solve_milp_problem
from solve.draw import draw_ilp_graph
from lin_prog.lp_matrix import LPMatrix
from lin_prog.lp_solver import solve_lp_problem

from solve.draw import draw_input_data
from solve.draw import draw_lp_graph
from solve.draw import draw_ilp_graph

import pandas as pd


G = Graph(gtw_pos, obj_pos, sta_pos, coverage, link_distance,
          gtw_lim, obj_lim, sta_lim,)
G.create_graph()

if problem is 'ILP':
    M = ILPMatrix(G)
    M.create_matrix()
    y_name = M.get_solution_col_name()
    # draw_graph(G, gtw_pos, obj_pos, sta_pos)
    x = solve_milp_problem(M.f.values,
                           M.int_constraints,
                           M.ineq_array.values,
                           M.ineq_b,
                           M.eq_array.values,
                           M.eq_b,
                           M.lower_bounds,
                           M.upper_bounds)

    solution = pd.Series(x, index=M.f.columns.values)
    placed_station = solution[y_name].values
    placed_station.tolist()
    draw_ilp_graph(G, gtw_pos, obj_pos, sta_pos, placed_station)

elif problem is 'LP':
    draw_input_data(gtw_pos, obj_pos, sta_pos)

    M = LPMatrix(G, gtw_lim, obj_lim, sta_lim)
    M.create_matrix()
    res = solve_lp_problem(M.f.values,
                           M.ineq_array.values,
                           M.ineq_b,
                           M.eq_array.values,
                           M.eq_b,
                           M.lower_bounds,
                           M.upper_bounds)

    solution = pd.Series(res.x, index=M.eq_array.columns.values)
    draw_lp_graph(G, gtw_pos, obj_pos, sta_pos,)

stop_debug_point = 'True'
