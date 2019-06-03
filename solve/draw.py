import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph):
    """
    Draw network graph
    :param graph: received graph of objects and stations
    :param position: input coordinates of the gateway, objects, stations
    :return: pyplot.show()
    """

    nx.draw_networkx_nodes(graph.G, graph.pos,
                           nodelist=graph.g_key, node_shape='s',
                           node_color='r', linewidths=3)
    nx.draw_networkx_nodes(graph.G, graph.pos,
                           nodelist=graph.o_key, node_shape='o',
                           node_color='b', linewidths=3)
    nx.draw_networkx_nodes(graph.G, graph.pos,
                           nodelist=graph.s_key, node_shape='^',
                           node_color='r', linewidths=3)
    nx.draw_networkx_edges(graph.G, graph.pos,
                           arrowsize=20, edge_color='b')
    nx.draw_networkx_labels(graph.G, graph.pos, font_color='w')

    fig = plt.gcf()
    ax = fig.gca()
    for i in graph.s_key:
        coverage = plt.Circle(graph.s_p[i], graph.coverage[i],
                              color='r', alpha=0.1)
        ax.add_artist(coverage)

        # link_distance = plt.Circle(graph.s_p[i],
        #                            graph.link_distance[i],
        #                            color='b', alpha=0.1)
        # ax.add_artist(link_distance)
    ax.axis('equal')

    plt.xlim([-5, 15])
    plt.ylim([-5, 15])
    plt.grid()
    plt.show()

