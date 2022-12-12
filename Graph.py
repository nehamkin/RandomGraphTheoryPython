import random
import networkx as nx
from networkx import fast_gnp_random_graph
from numpy import average


def get_probability(n, lam, c):
    # eps = lam * n ^ (-1/3)
    return c / n


def create_graph(n, lam, c):
    p = get_probability(n, lam, c)
    graph = fast_gnp_random_graph(n, p)
    return graph


def get_components(graph):
    return [c for c in nx.connected_components(graph)]


def get_components_subgraphs(graph):
    return [graph.subgraph(c).copy() for c in nx.connected_components(graph)]


def get_largest_component(graph):
    components = get_components(graph)
    max_component = max(components, key=len)
    return max_component


def get_comlexity_of_component(graph):
    return len(graph.edges) - len(graph.nodes) + 1


def get_complexity_of_components(graph):
    subgraphs = get_components_subgraphs(graph)
    return [get_comlexity_of_component(subgraph) for subgraph in subgraphs]


def max_averages (i, n, c):
    temp_maxes = []
    for j in range(1, 50):
        graph = create_graph(i * 100, 0, c)
        temp_maxes.append(len(get_largest_component(graph)))
    return average(temp_maxes)


def create_graphs(n, c):
    max_components = []
    for i in range(1, n + 1):
        max_averages(100, i * 100, c)
    return max_components


def create_plot(max_components):
    import matplotlib.pyplot as plt
    plt.plot([i * 100 for i in range(1, len(max_components)+1)], max_components)
    plt.xlabel('n')
    plt.ylabel('max component size')
    plt.show()


def experiment(n, c):
    max_components = create_graphs(n, c)
    create_plot(max_components)
