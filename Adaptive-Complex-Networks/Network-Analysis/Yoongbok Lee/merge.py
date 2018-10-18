import matplotlib.pyplot as plt
import networkx as nx
import random


def random_color():
    hex_digits = [0,0,0,0,0,0]
    for i in range(len(hex_digits)):
        hex_digits[i] = random.randint(0,15)
    result = "#"
    for dig in hex_digits:
        result = result + hex(dig).split('x')[-1]
    if result == "#000000" or result == "#FFFFFF":
        result = random_color()
    return result


def color_cliques(G):
    """hubs(cliques) are all complete subgraphs of G"""
    p = dict(nx.single_source_shortest_path_length(G, ncenter))
    cliques = list(nx.algorithms.clique.find_cliques(G))
    for v in p:
        # default color is blue
        p[v] = '#DDDDDD'
    # order cliques in descending order depending on size
    cliques.sort(key=len, reverse=True)

    for clique in cliques:
        clique.sort()

    for clique in cliques:
        if len(clique) > 3:
            clique_color = random_color()
            for node in clique:
                p[node] = clique_color
            for node in clique:
                for clique in cliques:
                    if node in clique:
                        cliques.remove(clique)
    return p


def color_neighbors(G):
    """possibility of robustness loss"""
    p = dict(nx.single_source_shortest_path_length(G, ncenter))
    neighbor = {}
    print(len(G))
    for node in G:
        neighbor[node] = len(list(nx.all_neighbors(G, node)))
    for value in neighbor:
        if (int(neighbor[value]) > 10):
            color = random_color()
            p[value] = color
            for node in nx.all_neighbors(G,value):
                p[node] = color
        else :
            p[value] = 'grey'
    return p


if __name__ == "__main__":
    my_float = 0.003
    this_float = 0.1
    G = nx.random_geometric_graph(500, this_float)
    print(G.number_of_edges())
    # position is stored as node attribute data for random_geometric_graph
    pos = nx.get_node_attributes(G, 'pos')
    G2 = nx.random_geometric_graph(200, this_float)
    """
    while(nx.number_connected_components(G2) < 2):
        count += 1
        this_float -= my_float
        G = G2
        G2 = nx.random_geometric_graph(200,this_float)
    """
    print(nx.number_connected_components(G), "connected components")
    print(this_float)
    # find node near center (0.5,0.5)
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d

    # p = color_cliques(G)
    p = color_neighbors(G)

    plt.figure(figsize=(8, 8))
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=list(p.keys()),
                           node_size=30,
                           node_color=list(p.values()),
                           cmap=plt.cm.Reds_r)
    # nx.draw_networkx(G,pos)
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.axis('off')
    plt.show()

    # print(nx.clustering(G))
    # print(list(nx.algorithms.clique.find_cliques(G)))
    # print(mylist[:10])
    print(nx.nodes(G)[0])
    # for c in list(nx.algorithms.clique.find_cliques(G)):
    #     if len(c) > 3:
    #         print(c,end=' ')
    # print(nx.attr_matrix(G))
    # for c in (nx.algorithms.community.k_clique_communities(G,2)):
    #     print(c)
