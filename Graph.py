import random
import networkx as nx
import numpy as np
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


def max_averages_of_graph(number_of_tries_per_graph, n, c):
    temp_maxes = []
    for j in range(0, number_of_tries_per_graph):
        graph = create_graph(n, 0, c)
        temp_maxes.append(len(get_largest_component(graph)))
    return average(temp_maxes)


def create__max_components_for_graphs(number_of_graphs, size_of_jumps, number_of_tries_per_graph, c):
    max_components = []
    for i in range(1, number_of_graphs + 1):
        n = i * size_of_jumps
        max_components.append(max_averages_of_graph(number_of_tries_per_graph, n, c))
    return max_components


def create_plot(max_components, size_of_jumps, c):
    import matplotlib.pyplot as plt
    plt.plot([i * size_of_jumps for i in range(1, len(max_components) + 1)], max_components)
    plt.xlabel('n')
    plt.ylabel('max component size')
    plt.title('c = ' + str(c))
    plt.show()


def experiment_number1_very_sub_critical_max_components_theta_ln():
    number_of_graphs = 150
    size_of_jumps = 1000
    number_of_tries_per_graph = 10
    for c in [0.25, 0.5, 0.75]:
        max_components = create__max_components_for_graphs(number_of_graphs, size_of_jumps, number_of_tries_per_graph,
                                                           c)
        create_plot(max_components, size_of_jumps, c)


def experiment_number1_very_sub_critical_simple_graphs():
    num_experiments = 1
    ns = [100000, 250000, 500000]
    for c in [0.9, 0.95, 0.99]:
        complexities_list = []
        for n in ns:
            mapped_complexities_list = []
            for i in range(0, num_experiments):
                graph = create_graph(n, 0, c)
                mapped_complexities = map_complexities(get_complexity_of_components(graph))
                mapped_complexities_list.append(mapped_complexities)
            complexity_average = average_counter_mapped_complexities_list(mapped_complexities_list)
            complexities_list.append(complexity_average)
        print(complexities_list)
        create_bar_complexities(complexities_list, ns, c)


def create_bar_complexities(complexities_list, ns, c):
    import matplotlib.pyplot as plt
    bar_width = 0.25
    br = np.arange(len(ns))
    n100 = [0] * (len(complexities_list[0]))
    for complexity in complexities_list[0]:
        print(complexity)
        print(complexities_list[0][complexity])
        n100[complexity] = complexities_list[0][complexity]
    n250 = [0] * (len(complexities_list[1]))
    for complexity in complexities_list[1]:
        n250[complexity] = complexities_list[1][complexity]
    n500 = [0] * (len(complexities_list[2]))
    for complexity in complexities_list[2]:
        n500[complexity] = complexities_list[2][complexity]
    br100 = np.arange(len(n100))
    br250 = [x + bar_width for x in br100]
    br500 = [x + bar_width for x in br250]

    plt.bar(br100, n100, color='r', width=bar_width, edgecolor='grey', label='n = 100000')
    plt.bar(br250, n250, color='g', width=bar_width, edgecolor='grey', label='n = 250000')
    plt.bar(br500, n500, color='b', width=bar_width, edgecolor='grey', label='n = 500000')

    plt.xlabel('complexity', fontweight='bold')
    plt.ylabel('number of components', fontweight='bold')
    plt.xticks([r + bar_width for r in range(len(n100))], complexities_list[0].keys())
    plt.title('c = ' + str(c))
    plt.legend()
    plt.show()


def map_complexities(complexities):
    from collections import Counter
    return Counter(complexities)


def average_counter_mapped_complexities_list(mapped_complexities_list):
    sum_map = {}
    for complexities in mapped_complexities_list:
        for complexity in complexities:
            if complexity in sum_map:
                sum_map[complexity] += complexities[complexity]
            else:
                sum_map[complexity] = complexities[complexity]
    for complexity in sum_map:
        sum_map[complexity] /= len(mapped_complexities_list)
    return sum_map
