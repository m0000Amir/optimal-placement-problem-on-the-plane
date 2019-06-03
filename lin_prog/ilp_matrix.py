from itertools import product
from itertools import permutations
import pandas as pd
import numpy as np


class ILPMatrix:
    """
    Prepare an input matrix for integer linear programming solver
    """
    def __init__(self, graph, s_num, g_lim, o_lim, s_lim):
        self.s_num = s_num
        self.v = {**g_lim, **o_lim, **s_lim}
        self.graph = graph
        self.mat = graph.adj_matrix.toarray()
        self.f = None
        self.int_constraints = None
        self.lower_bounds = None
        self.upper_bounds = None
        self.eq_array = None
        self.eq_b = None
        self.ineq_array = None
        self.ineq_b = None

    @staticmethod
    def create_x_name(edge_name):
        return ['x' + ''.join(map(str, edge_name[i]))
                for i in range(len(edge_name))]

    def create_edge_name(self):
        g_k = ''.join(map(str, self.graph.g_key))
        o_k = ''.join(map(str, self.graph.o_key))
        s_k = ''.join(map(str, self.graph.s_key))

        o_s = [i for i in product(o_k, s_k)]
        s_s = [i for i in permutations(s_k, 2)]
        s_g = [i for i in product(s_k, g_k)]

        o_s_name = self.create_x_name(o_s)
        s_s_name = self.create_x_name(s_s)
        s_g_name = self.create_x_name(s_g)

        return o_s_name + s_s_name + s_g_name

    def create_value_name(self, w_num):
        x = self.create_edge_name()
        y = ['y' + str(i) for i in self.graph.s_key]
        w = ['w' + str(i) for i in range(w_num)]

        return [x, y, w]

    def make_int_constraints(self, name):
        column, = np.where(np.in1d(self.f.columns.values, name))
        return [i + 1 for i in column]

    def make_objective(self, col, w):
        """
        make objective function
        :param col: column name vector
        :param w: mame of w parameter vector
        :return: self.f
        """
        data = np.zeros([1, len(col)]).astype(int)
        self.f = pd.DataFrame(data, columns=col)
        column, = np.where(np.in1d(self.f.columns.values, w))
        self.f.iloc[0, column] = 1

        self.lower_bounds = np.zeros([1, len(col)]).astype(int)
        self.upper_bounds = np.ones([1, len(col)]).astype(int) * np.inf

    def make_for_g(self, i):
        row_mat, = np.where(self.mat[:, i] == 1)
        mat_name = ['x' + str(row_mat[j]) + str(i) for j in range(len(row_mat))]

        column, = np.where(np.in1d(self.eq_array.columns.values, mat_name))
        self.eq_array.iloc[i, column] = 1
        self.eq_array.ix[i, 'w' + str(i)] = 1
        self.eq_b[i] = sum(self.v[j] for j in self.graph.o_key)

    def make_for_o(self, i):
        col_mat, = np.where(self.mat[i, :] == 1)
        mat_name = ['x' + str(i) + str(col_mat[j]) for j in range(len(col_mat))]

        column, = np.where(np.in1d(self.eq_array.columns.values, mat_name))
        self.eq_array.iloc[i, column] = 1
        self.eq_array.ix[i, 'w' + str(i)] = 1
        self.eq_b[i] = self.v[i]

    def add_input_edge_s(self, i, array):
        row_mat, = np.where(self.mat[:, i] == 1)
        mat_name_plus = ['x' + str(row_mat[j]) + str(i)
                         for j in range(len(row_mat))]

        column_plus, = np.where(np.in1d(array.columns.values,
                                        mat_name_plus))
        array.iloc[i, column_plus] = 1

    def make_eq_for_s(self, i, array):

        self.add_input_edge_s(i, array)

        col_mat, = np.where(self.mat[i, :] == 1)
        mat_name_minus = ['x' + str(i) + str(col_mat[j])
                          for j in range(len(col_mat))]
        column_minus, = np.where(np.in1d(array.columns.values,
                                         mat_name_minus))
        array.iloc[i, column_minus] = -1

        array.ix[i, 'w' + str(i)] = 1
        self.eq_b[i] = 0

    @staticmethod
    def make_eq_for_y(i, y, array, coefficient=1):
        column, = np.where(np.in1d(array.columns.values, y))
        array.iloc[i, column] = coefficient

    def make_equality(self, row, y):
        for i in range(row + 1):
            if i in self.graph.g_key:
                self.make_for_g(i)

            if i in self.graph.o_key:
                self.make_for_o(i)

            if i in self.graph.s_key:
                self.make_eq_for_s(i, self.eq_array)

            if i == row:
                self.make_eq_for_y(i, y, self.eq_array)
                self.eq_b[i] = self.s_num

    def make_inequality(self):
        for i in self.graph.s_key:
            self.add_input_edge_s(i, self.ineq_array)
            coef = -1 * self.v[i]
            self.make_eq_for_y(i, 'y' + str(i), self.ineq_array, coef)

    def create_matrix(self):
        """
        Input matrices of integer linear programming problem

        :return: equality matrix, linear equality constraint vector;
         inequality matrix, linear inequality constraint vector;
         upper bounds vector; lower bounds vector
        """
        row_num = (len(self.graph.g_key) +
                   len(self.graph.o_key) +
                   len(self.graph.s_key))

        [x_name, y_name, w_name] = self.create_value_name(row_num)
        col_name = x_name + y_name + w_name

        self.make_objective(col_name, w_name)
        self.int_constraints = self.make_int_constraints(y_name)

        data_eq = np.zeros([row_num + 1, len(col_name)]).astype(int)
        self.eq_b = np.zeros(row_num + 1)
        self.eq_array = pd.DataFrame(data_eq, columns=col_name)

        self.make_equality(row_num, y_name)

        data_ineq = np.zeros([row_num + 1, len(col_name)]).astype(int)
        self.ineq_b = np.zeros(row_num + 1)
        self.ineq_array = pd.DataFrame(data_ineq, columns=col_name)

        self.make_inequality()




