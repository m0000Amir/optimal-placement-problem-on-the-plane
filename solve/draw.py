import networkx as nx
import matplotlib.pyplot as plt
import itertools


def get_coordinates(position):
    point = position.values()
    x, y = zip(*point)
    return x, y


def draw_input_data(g_p, o_p, s_p,):
    plt.close()
    fig = plt.gcf()
    ax = fig.gca()
    g_x, g_y = get_coordinates(g_p)
    plt.plot(g_x, g_y, color='r', marker='s', markersize=20, linestyle='')
    [plt.annotate(i, xy=g_p[i], xytext=g_p[i], ha='center', va='center',
                  color='w') for i in g_p]

    o_x, o_y = get_coordinates(o_p)
    plt.plot(o_x, o_y, color='b', marker='o', markersize=20, linestyle='')
    [plt.annotate(i, xy=o_p[i], xytext=o_p[i], ha='center', va='center',
                  color='w') for i in o_p]

    s_x, s_y = get_coordinates(s_p)
    plt.plot(s_x, s_y, color='#FF9999', marker='o', markersize=20, linestyle='')
    [plt.annotate(i, xy=s_p[i], xytext=s_p[i], ha='center', va='center',
                  color='w') for i in s_p]

    ax.axis('equal')
    plt.grid()
    plt.show()


def prepare_graph_for_draw(graph, s_p, placed_sta):
    pos = graph.pos.copy()
    draw_graph_node = graph.G.copy()

    sta_node = graph.s_key
    cov_sta = graph.cov * len(list(s_p.keys()))
    cov_sta.sort()

    sta = list(itertools.compress(graph.s_key, placed_sta))
    cov = list(itertools.compress(cov_sta, placed_sta))
    sta_name = list(
        itertools.compress(list(s_p.keys()) * len(graph.cov), placed_sta))

    remote_node = [i for i in sta_node if i not in sta]

    draw_graph_node.remove_nodes_from(remote_node)
    dict(pos.pop(i) for i in remote_node)

    key = list(draw_graph_node.node)
    value = key.copy()
    [value.remove(i) for i in sta]
    labels = dict(zip(key, value + sta_name))
    return [draw_graph_node, pos, labels, sta, cov]


def draw_ilp_graph(graph, g_p, o_p, s_p, placed_sta):
    """
    Draw network graph
    :param graph:  received graph of objects and stations
    :param g_p: gateway position
    :param o_p: object position
    :param s_p: station position
    :param placed_sta: placed station selectors after solving the problem
    :return: ILP problem graph
    """
    draw_g_node, pos, labels, sta, cov = prepare_graph_for_draw(graph, s_p,
                                                                placed_sta)

    nx.draw_networkx_nodes(draw_g_node, pos,
                           nodelist=g_p.keys(), node_shape='s',
                           node_color='r', linewidths=3)
    nx.draw_networkx_nodes(draw_g_node, pos,
                           nodelist=o_p.keys(), node_shape='o',
                           node_color='b', linewidths=3)
    nx.draw_networkx_nodes(draw_g_node, pos,
                           nodelist=sta, node_shape='^',
                           node_color='r', linewidths=3)
    nx.draw_networkx_edges(draw_g_node, pos,
                           arrowsize=20, edge_color='b')

    nx.draw_networkx_labels(draw_g_node, pos, labels=labels, font_color='w')
    fig = plt.gcf()
    ax = fig.gca()
    for i in range(len(sta)):
        coverage = plt.Circle(graph.s_p[sta[i]], cov[i],
                              color='r', alpha=0.1)
        ax.add_artist(coverage)
    ax.axis('equal')
    plt.grid()
    plt.show()


def draw_lp_graph(graph, gtw_pos, obj_pos, sta_pos):
    """
    Draw network graph of LP problem
    :param graph:  received graph of objects and stations
    :param gtw_pos: gateway position
    :param obj_pos: object position
    :param sta_pos: station position
    :return: LP problem graph
    """
    g_list = list(gtw_pos.keys())
    o_list = list(obj_pos.keys())
    s_list = list(sta_pos.keys())

    nx.draw_networkx_nodes(graph.G, graph.pos,
                           nodelist=g_list, node_shape='s',
                           node_color='r', linewidths=10)
    nx.draw_networkx_nodes(graph.G, graph.pos,
                           nodelist=o_list, node_shape='o',
                           node_color='b', linewidths=5)
    nx.draw_networkx_nodes(graph.G, graph.pos,
                           nodelist=s_list, node_shape='^',
                           node_color='r', linewidths=10)
    nx.draw_networkx_edges(graph.G, graph.pos,
                           arrowsize=20, edge_color='b')
    nx.draw_networkx_labels(graph.G, graph.pos, font_color='w')

    # for i in range(len(sta)):
    #     coverage = plt.Circle(graph.s_p[sta[i]], graph.cov[i],
    #                           color='r', alpha=0.1)
    #     ax.add_artist(coverage)
    # ax.axis('equal')
    # plt.grid()
    # plt.show()

    plt.grid()
    plt.show()

