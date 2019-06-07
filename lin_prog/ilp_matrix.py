from itertools import product, permutations, compress
import pandas as pd
import numpy as np


class ILPMatrix:
    """
    Prepare an input matrix for integer linear programming solver
    """
    def __init__(self, graph):
        self.graph = graph
        self.mat = graph.adj_matrix.toarray()
        # Input matrices for ILP problem
        self.f = None
        self.int_constraints = None
        self.lower_bounds = None
        self.upper_bounds = None
        self.eq_array = None
        self.eq_b = None
        self.ineq_array = None
        self.ineq_b = None
        self._splacenum = int(len(self.graph.s_p) / len(self.graph.cov))

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
        self.eq_b[i] = sum(self.graph.o_lim.values())

    def make_for_o(self, i):
        col_mat, = np.where(self.mat[i, :] == 1)
        mat_name = ['x' + str(i) + str(col_mat[j]) for j in range(len(col_mat))]

        column, = np.where(np.in1d(self.eq_array.columns.values, mat_name))
        self.eq_array.iloc[i, column] = 1
        self.eq_array.ix[i, 'w' + str(i)] = 1
        self.eq_b[i] = self.graph.o_lim[i]

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

    # def make_eq_for_var_param(self, row, y):
    #     step = int(len(self.graph.s_p) / len(self.graph.cov))
    #     for i in range(0, step):
    #         selectors = [0] * len(self.graph.s_p)
    #         [selectors.insert(i, 1) for i in range(i, len(self.graph.s_p), 3)]
    #         y_name = list(compress(y, selectors))
    #
    #         self.make_eq_for_y(row + i, y_name, self.ineq_array)
    #         self.ineq_b[row + i] = 1

    def make_eq_for_var_param(self, row, y):
        for i in range(0, len(self.graph.cov)):
            y_name = [y[j+i*self._splacenum] for j in range(0,self._splacenum)]

            self.make_eq_for_y(row + i, y_name, self.ineq_array)
            self.ineq_b[row + i] = 1

    def make_equality(self, row, col, y):

        data_eq = np.zeros([row + 1, len(col)]).astype(int)
        self.eq_b = np.zeros(row + 1)
        self.eq_array = pd.DataFrame(data_eq, columns=col)

        for i in range(row + 1):
            if i in self.graph.g_key:
                self.make_for_g(i)

            if i in self.graph.o_key:
                self.make_for_o(i)

            if i in self.graph.s_key:
                self.make_eq_for_s(i, self.eq_array)

            if i == row:
                self.make_eq_for_y(i, y, self.eq_array)
                self.eq_b[i] = len(self.graph.cov)

        # if len(self.graph.cov) is not 1:
        #     self.make_eq_for_var_param(row, y)

    def make_inequality(self, row, col, y):
        if len(self.graph.cov) is not 1:
            # additional conditions for stations with various parameters
            data_row = (row + len(self.graph.cov))
        else:
            data_row = row
        data_ineq = np.zeros([data_row, len(col)]).astype(int)
        self.ineq_b = np.zeros(data_row)
        self.ineq_array = pd.DataFrame(data_ineq, columns=col)

        for i in self.graph.s_key:
            self.add_input_edge_s(i, self.ineq_array)
            coef = -1 * self.graph.s_lim[i]
            self.make_eq_for_y(i, 'y' + str(i), self.ineq_array, coef)
        if len(self.graph.cov) is not 1:
            self.make_eq_for_var_param(row, y)

    def create_matrix(self):
        """
        Input matrices of integer linear programming problem

        :return: equality matrix, linear equality constraint vector;
         inequality matrix; linear inequality constraint vector;
         upper bounds vector; lower bounds vector
        """

        row_num = (len(self.graph.g_key) + len(self.graph.o_key) +
                   len(self.graph.s_key))

        [x_name, y_name, w_name] = self.create_value_name(row_num)
        col_name = x_name + y_name + w_name

        self.make_objective(col_name, w_name)
        self.int_constraints = self.make_int_constraints(y_name)

        # data_eq = np.zeros([row_num + 1, len(col_name)]).astype(int)
        # self.eq_b = np.zeros(row_num + 1)
        # self.eq_array = pd.DataFrame(data_eq, columns=col_name)
        # if len(self.graph.cov) is not 1:
        #     # additional conditions for stations with various parameters
        #     datasize = (row_num + 1 +
        #                 int(len(self.graph.s_p) / len(self.graph.cov)))
        # else:
        #     datasize = row_num + 1
        # eq_row_size = row_num + 1
        self.make_equality(row_num, col_name, y_name)

        # data_ineq = np.zeros([row_num + 1, len(col_name)]).astype(int)
        # self.ineq_b = np.zeros(row_num + 1)
        # self.ineq_array = pd.DataFrame(data_ineq, columns=col_name)
        # if len(self.graph.cov) is not 1:
        #     # additional conditions for stations with various parameters
        #     ineq_row_size = (row_num +
        #                        int(len(self.graph.s_p) / len(self.graph.cov)))
        # else:
        #     ineq_row_size = row_num

        self.make_inequality(row_num, col_name, y_name)

    def get_solution_col_name(self):
        row_num = (len(self.graph.g_key) + len(self.graph.o_key) +
                   len(self.graph.s_key))
        [x_name, y_name, w_name] = self.create_value_name(row_num)
        column, = np.where(np.in1d(self.f.columns.values, y_name))

        name = ['y' + str(self.graph.s_key[0] + j) + '_s_' + str(i + 1)
                for i in range(0, len(self.graph.cov))
                for j in range(0, self._splacenum)]
        self.f.columns.values[column] = name
        return name
