import itertools
import math

from problem.input import gtw_pos, obj_pos, sta_pos
from problem.input import cost, coverage, link_distance, limit
from problem.input import gtw_lim, obj_lim#, s_num

import networkx as nx


class Graph:
    """
    Building objects and service stations network graph
    """
    def __init__(self):
        # self.m = s_num
        self.g_p = gtw_pos
        self.s_p = sta_pos
        self.o_p = obj_pos
        self.g_key = list(self.g_p.keys())
        self.o_key = list(self.o_p.keys())
        self.s_key = list(self.s_p.keys())
        self.cov = coverage
        self.link = link_distance
        self.limit = limit
        self.g_lim = gtw_lim
        self.o_lim = obj_lim
        # self.s_lim = sta_lim

        self.G = nx.DiGraph()
        self.s_lim = None
        self.pos = None
        self.coverage = None
        self.link_distance = None
        self.adj_matrix = None

        self.s_origin = list(self.s_p.keys())

    def check_o2g_path(self):
        gateway = self.g_key[0]
        paths_exist = all([nx.has_path(self.G, i, gateway) for i in self.o_key])
        assert paths_exist, ('The graph does not link '
                             'all objects with the gateway')

    def prepare_param_sta(self):
        """
        prepare parameters of stations and positions
        :return: self.coverage : dict; self.link_distance : dict;
        self.pos : dict
        """
        # _cov = self.cov * len(self.s_key)
        # _cov.sort()
        _cov = list(j for i in [[k] * len(self.s_key)
                                for k in self.cov] for j in i)
        self.coverage = {k + self.s_key[0]: value
                         for k, value in enumerate(_cov)}

        _link = self.link * len(self.s_key)
        _link.sort()
        self.link_distance = {k + self.s_key[0]: value
                              for k, value in enumerate(_link)}

        _lim = self.limit * len(self.s_key)
        _lim.sort()
        self.s_lim = {k + self.s_key[0]: value for k, value in enumerate(_lim)}

        _s_pos = list(self.s_p.values()) * len(self.cov)
        self.s_p = {k + self.s_key[0]: value
                    for k, value in enumerate(_s_pos)}
        self.pos = {**self.g_p, **self.o_p, **self.s_p}
        self.G.add_nodes_from([i for i in range(len(self.g_p) +
                                                len(self.s_p) +
                                                len(self.o_p))])

        _s_lim = list(self.s_lim.values()) * len(self.cov)
        self.s_lim = {k + self.s_key[0]: value
                      for k, value in enumerate(_s_lim)}
        self.g_key = list(self.g_p.keys())
        self.o_key = list(self.o_p.keys())
        self.s_key = list(self.s_p.keys())

    def check_coverage(self, i, j):
        sta2obj_dist = math.sqrt((self.o_p[i][0] - self.s_p[j][0]) ** 2 +
                                 (self.o_p[i][1] - self.s_p[j][1]) ** 2)
        return sta2obj_dist < self.coverage[j]

    def check_distance(self, i, j):
        sta2sta_dist = math.sqrt((self.s_p[i][0] - self.s_p[j][0]) ** 2 +
                                 (self.s_p[i][1] - self.s_p[j][1]) ** 2)
        return sta2sta_dist < self.link_distance[i]

    @staticmethod
    def make_edge(i, j, point1, point2, param):
        distance = math.sqrt((point1[i][0] - point2[j][0]) ** 2 +
                             (point1[i][1] - point2[j][1]) ** 2)
        return distance < param[i]

    def create_graph(self):
        """
        get network graph
        :return: adjacency matrix
        """
        self.prepare_param_sta()
        # add edge of object2station
        for o2s in itertools.product(self.o_p.keys(), self.s_p.keys()):
            if self.make_edge(o2s[1], o2s[0],
                              self.s_p, self.o_p, self.coverage):
                self.G.add_edge(o2s[0], o2s[1])

        # add edge of station2station
        for s2s in itertools.permutations(self.s_p.keys(), 2):
            if self.make_edge(s2s[0], s2s[1],
                              self.s_p, self.s_p, self.link_distance):
                self.G.add_edge(s2s[0], s2s[1])

        # add edge of station2gateway
        for s2g in itertools.product(self.s_p.keys(), self.g_p.keys()):
            if self.make_edge(s2g[0], s2g[1],
                              self.s_p, self.g_p, self.link_distance):
                self.G.add_edge(s2g[0], s2g[1])

        self.check_o2g_path()

        self.adj_matrix = nx.adjacency_matrix(self.G)


class GraphCP:
    """
    Building objects and service stations network graph for cost problem
    """
    def __init__(self):
        # self.m = s_num
        self.g_p = gtw_pos
        self.s_p = sta_pos
        self.o_p = obj_pos
        self.g_key = list(self.g_p.keys())
        self.o_key = list(self.o_p.keys())
        self.s_key = list(self.s_p.keys())
        self.cost = cost
        self.cov = coverage
        self.link = link_distance
        self.limit = limit
        self.g_lim = gtw_lim
        self.o_lim = obj_lim
        # self.s_lim = sta_lim

        self.G = nx.DiGraph()
        self.s_lim = None
        self.pos = None
        self.cost_sta = None
        self.coverage = None
        self.link_distance = None
        self.adj_matrix = None

        self.s_origin = list(self.s_p.keys())

    def check_o2g_path(self):
        gateway = self.g_key[0]
        for i in self.o_key:
            a = nx.has_path(self.G, i, gateway)
        paths_exist = all([nx.has_path(self.G, i, gateway) for i in self.o_key])
        assert paths_exist, \
            'The graph does not link all objects with the gateway'

    def prepare_param_sta(self):
        """
        prepare parameters of stations and positions
        :return: self.coverage : dict; self.link_distance : dict;
        self.pos : dict
        """
        # _cov = self.cov * len(self.s_key)
        # _cov.sort()

        _cost = list(j for i in [[k] * len(self.s_key)
                                 for k in self.cost] for j in i)
        self.cost_sta = {k + self.s_key[0]: value
                         for k, value in enumerate(_cost)}

        _cov = list(j for i in [[k] * len(self.s_key)
                                for k in self.cov] for j in i)
        self.coverage = {k + self.s_key[0]: value
                         for k, value in enumerate(_cov)}

        _link = self.link * len(self.s_key)
        _link.sort()
        self.link_distance = {k + self.s_key[0]: value
                              for k, value in enumerate(_link)}

        _lim = self.limit * len(self.s_key)
        _lim.sort()
        self.s_lim = {k + self.s_key[0]: value for k, value in enumerate(_lim)}

        _s_pos = list(self.s_p.values()) * len(self.cov)
        self.s_p = {k + self.s_key[0]: value
                    for k, value in enumerate(_s_pos)}
        self.pos = {**self.g_p, **self.o_p, **self.s_p}
        self.G.add_nodes_from([i for i in range(len(self.g_p) +
                                                len(self.s_p) +
                                                len(self.o_p))])

        _s_lim = list(self.s_lim.values()) * len(self.cov)
        self.s_lim = {k + self.s_key[0]: value
                      for k, value in enumerate(_s_lim)}
        self.g_key = list(self.g_p.keys())
        self.o_key = list(self.o_p.keys())
        self.s_key = list(self.s_p.keys())

    def check_coverage(self, i, j):
        sta2obj_dist = math.sqrt((self.o_p[i][0] - self.s_p[j][0]) ** 2 +
                                 (self.o_p[i][1] - self.s_p[j][1]) ** 2)
        return sta2obj_dist < self.coverage[j]

    def check_distance(self, i, j):
        sta2sta_dist = math.sqrt((self.s_p[i][0] - self.s_p[j][0]) ** 2 +
                                 (self.s_p[i][1] - self.s_p[j][1]) ** 2)
        return sta2sta_dist < self.link_distance[i]

    @staticmethod
    def make_edge(i, j, point1, point2, param):
        distance = math.sqrt((point1[i][0] - point2[j][0]) ** 2 +
                             (point1[i][1] - point2[j][1]) ** 2)
        return distance < param[i]

    def create_graph(self):
        """
        get network graph
        :return: adjacency matrix
        """
        self.prepare_param_sta()
        # add edge of object2station
        for o2s in itertools.product(self.o_p.keys(), self.s_p.keys()):
            if self.make_edge(o2s[1], o2s[0],
                              self.s_p, self.o_p, self.coverage):
                self.G.add_edge(o2s[0], o2s[1])

        # add edge of station2station
        for s2s in itertools.permutations(self.s_p.keys(), 2):
            if self.make_edge(s2s[0], s2s[1],
                              self.s_p, self.s_p, self.link_distance):
                self.G.add_edge(s2s[0], s2s[1])

        # add edge of station2gateway
        for s2g in itertools.product(self.s_p.keys(), self.g_p.keys()):
            if self.make_edge(s2g[0], s2g[1],
                              self.s_p, self.g_p, self.link_distance):
                self.G.add_edge(s2g[0], s2g[1])

        self.check_o2g_path()

        self.adj_matrix = nx.adjacency_matrix(self.G)
