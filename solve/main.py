from problem.input import problem

from solve.network import Graph
from solve.network import GraphCP
from lin_prog.ilp_matrix import ILPMatrix
from lin_prog.ilp_matrix_cp import ILPCostProblemMatrix
from lin_prog.milp_solver import solve_milp_problem
from lin_prog.milp_cp_solver import solve_milp_cp_problem
from lin_prog.lp_matrix import LPMatrix
from lin_prog.lp_solver import solve_lp_problem

from solve.draw import draw_input_data
from solve.draw import draw_lp_graph
from solve.draw import draw_ilp_graph

import pandas as pd

import time

start_time = time.time()

if problem is 'ILP':
    G = Graph()
    G.create_graph()
    M = ILPMatrix(G)
    M.create_matrix()
    y_name = M.get_solution_col_name()
    draw_input_data()
    x = solve_milp_problem(M.f.values,
                           M.int_constraints,
                           M.ineq_array.values,
                           M.ineq_b,
                           M.eq_array.values,
                           M.eq_b,
                           M.lower_bounds,
                           M.upper_bounds)

    solution = pd.Series(x, index=M.f.columns.values).T
    placed_station = solution[y_name].values
    placed_station.tolist()
    draw_ilp_graph(G, placed_station, y_name)

elif problem is 'ILPcp':
    draw_input_data()
    G = GraphCP()
    G.create_graph()

    M = ILPCostProblemMatrix(G)
    M.create_matrix()
    y_name = M.get_solution_col_name()
    x, f = solve_milp_cp_problem(M.f.values,
                           M.int_constraints,
                           M.ineq_array.values,
                           M.ineq_b,
                           M.eq_array.values,
                           M.eq_b,
                           M.lower_bounds,
                           M.upper_bounds)

    solution = pd.Series(x, index=M.f.columns.values).T
    placed_station = solution[y_name].values
    placed_station.tolist()
    draw_ilp_graph(G, placed_station, y_name)
    print('f =  ', f )

elif problem is 'LP':
    G = Graph()
    G.create_graph()
    # to place objects, stations and gateway on coordinate plane
    draw_input_data()

    M = LPMatrix(G)
    M.create_matrix()
    res = solve_lp_problem(M.f.values,
                           M.ineq_array.values,
                           M.ineq_b,
                           M.eq_array.values,
                           M.eq_b,
                           M.lower_bounds,
                           M.upper_bounds)

    solution = pd.Series(res.x, index=M.eq_array.columns.values)
    draw_lp_graph(G)


print("--- %.2f seconds ---" % (time.time() - start_time))

""""
to correct upper bounds"""
