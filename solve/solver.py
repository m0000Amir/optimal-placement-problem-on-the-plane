from solve.draw import draw_graph
from solve.network import Graph
from lin_prog.ilp_matrix import*
from lin_prog.mat_engine import milpsolver

G = Graph(gateway_coordinates, objects_coordinates, stations_coordinates,)
G.create_graph()

draw_graph(G.G, G.pos)


adj_matrix = G.adj_matrix.toarray()

M = ILPMatrix(adj_matrix)
M.create_matrix()
path = '../solve/matfiles/'
x, fval, exitflag, output = milpsolver(path,
                                       M.f.values,
                                       M.int_constraints,
                                       M.ub_array.values,
                                       M.ub_b,
                                       M.eq_array.values,
                                       M.eq_b,
                                       M.lower_bounds,
                                       M.upper_bounds)
print(fval)

