from merge import Merger
import networkx as nx
import matplotlib.pyplot as plt

g_list = []
for i in range(16):
    g_list.append(nx.Graph())

e_list_list = []
for j in range(16):
    e_list_list.append([])

e_list_list[0] = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [2, 4], [3, 5], [4, 5], [5, 6]]
e_list_list[1] = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [3, 5], [4, 5], [4, 6], [5, 6]]
e_list_list[2] = [[0, 1], [1, 2], [1, 3], [2, 3]]
e_list_list[3] = [[0, 1], [1, 2], [1, 3], [2, 3], [2, 4], [3, 4]]
e_list_list[4] = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 5], [2, 5], [3, 5], [4, 5]]
e_list_list[5] = [[0, 1], [0, 2], [1, 2], [1, 3], [3, 4], [2, 4], [3, 5], [4, 5], [5, 6]]
e_list_list[6] = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
e_list_list[7] = [[0, 1], [1, 2], [2, 3], [0, 3]]
e_list_list[8] = [[0, 1], [1, 2], [1, 3]]
e_list_list[9] = [[0, 1], [1, 2], [2, 3]]
e_list_list[10] = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 5], [2, 5], [3, 6], [4, 6], [5, 7], [5, 8], [6, 9], [6, 7],
                   [8, 9], [7, 10], [8, 10], [9, 10]]
e_list_list[11] = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 3], [2, 4], [4, 0]]
e_list_list[12] = [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [3, 5], [4, 5]]
e_list_list[13] = [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [3, 5], [4, 5]]
e_list_list[14] = [[0, 2], [1, 2], [2, 3], [2, 4], [4, 5], [2, 5], [5, 6], [5, 7], [5, 8]]
e_list_list[15] = [[0, 3], [1, 3], [2, 3], [3, 4], [3, 5], [3, 6], [5, 6], [5, 7], [6, 8]]

for i in range(len(e_list_list)):
    g = g_list[i]
    g.add_edges_from(e_list_list[i])
    plt.subplot()
    nx.draw(g, with_labels=True)
    plt.show()

    g_cont = Merger(g)
    print(nx.global_efficiency(g))
    g_cont.cont_all_cliques(min_clique_node=3)
    print(nx.global_efficiency(g_cont.graph))
    plt.subplot()
    nx.draw(g_cont.graph, with_labels=True)
    plt.show()
    # g_cont.print_concat_nodes()
