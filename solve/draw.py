from input.input import*
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph, position):
    """
    Draw network graph
    :param graph: received graph of objects and stations
    :param position: input coordinates of the gateway, objects, stations
    :return: pyplot.show()
    """

    g_list = list(gateway_coordinates.keys())
    o_list = list(objects_coordinates.keys())
    s_list = list(stations_coordinates.keys())

    nx.draw_networkx_nodes(graph, position,
                           nodelist=g_list, node_shape='s',
                           node_color='r', linewidths=10)
    nx.draw_networkx_nodes(graph, position,
                           nodelist=o_list, node_shape='o',
                           node_color='b', linewidths=5)
    nx.draw_networkx_nodes(graph, position,
                           nodelist=s_list, node_shape='^',
                           node_color='r', linewidths=10)
    nx.draw_networkx_edges(graph, position,
                           arrowsize=20, edge_color='b')
    nx.draw_networkx_labels(graph, position, font_color='w')
    plt.grid()
    plt.show()
