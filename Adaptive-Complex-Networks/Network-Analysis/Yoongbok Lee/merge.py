import matplotlib.pyplot as plt
import networkx as nx
import random


def random_color():
    """selecting random color in hex"""
    hex_digits = [0,0,0,0,0,0]
    for i in range(len(hex_digits)):
        hex_digits[i] = random.randint(0,15)
    result = "#"
    for dig in hex_digits:
        result = result + hex(dig).split('x')[-1]
    if result == "#000000" or result == "#FFFFFF":
        result = random_color()
    return result


def color_cliques(G, ncenter, min_node_num=3):
    """hubs(cliques) are complete subgraphs of G"""
    p_list = list(G.nodes)
    p = {}
    for thing in p_list:
        p[thing] = "#DDDDDD"

    cliques = list(nx.algorithms.clique.find_cliques(G))
    # order cliques in descending order depending on size
    cliques.sort(key=len, reverse=True)

    for clique in cliques:
        clique.sort()

    for clique in cliques:
        if len(clique) > min_node_num:
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

    for node in G:
        neighbor[node] = list(nx.all_neighbors(G, node))
    for value in neighbor:
        if int(len(neighbor[value])) > 10:
            color = random_color()
            p[value] = color
            for node in nx.all_neighbors(G, value):
                p[node] = color
        else :
            p[value] = 'grey'
    return p


def cont_all_cliques_iterative(G, min_clique_node=4):
    cliques = list(nx.algorithms.find_cliques(G))
    cliques.sort(key=len, reverse=True)
    while len(cliques[0]) > min_clique_node:
        clique = cliques[0]
        G = contract_clique(G, clique)
        cliques = list(nx.algorithms.find_cliques(G))
        cliques.sort(key=len, reverse=True)
    return G


def cont_all_cliques(G, min_clique_node=4):
    new = G
    cliques = list(nx.algorithms.find_cliques(G))
    cliques.sort(key=len, reverse=True)
    while len(cliques[0]) >= min_clique_node:
        clique = cliques[0]
        for node in clique:
            for c in cliques:
                if node in c and c != clique:
                    c.remove(node)
                    # cliques.remove(c)
        new = contract_clique(new, clique)
        cliques.remove(cliques[0])
        cliques.sort(key=len, reverse=True)
    return new


def cont_all_stars_iterative(G, min_neighbors=10):
    neighbor = {}
    result = G
    for node in G:
        try:
            neighbors = list(nx.all_neighbors(result, node))
        except nx.exception.NetworkXError:
            continue
        if len(neighbors) > min_neighbors:
            neighbor[node] = neighbors
            result = contract_star(result, node)
            result = nx.convert_node_labels_to_integers(result)
    return result


def contract_clique(G, clique):
    new = G
    rand = random.randint(0, len(clique)-1)
    center = clique[rand]
    clique.remove(center)
    for node in clique:
        # print(center, node)
        try:
            new = nx.contracted_nodes(G, center, node)
        except nx.exception.NetworkXError as e:
            print("error: ", e)
            print(center, node)
    return new


def contract_star(G, center):
    result = G
    for node in nx.all_neighbors(G, center):
        result = nx.contracted_nodes(result, center, node)
    return result

def draw_graph(G):
    print("# of edges:", G.number_of_edges())
    print("# of nodes:", G.number_of_nodes())
    # position is stored as node attribute data for random_geometric_graph
    pos = nx.get_node_attributes(G, 'pos')
    """
    while(nx.number_connected_components(G2) < 2):
        count += 1
        this_float -= my_float
        G = G2
        G2 = nx.random_geometric_graph(200,this_float)
    """
    print(nx.number_connected_components(G), "connected components")
    # find node near center (0.5,0.5)
    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d

    p = color_cliques(G, ncenter)

    plt.figure(1,figsize=(8, 8))
    plt.subplot()
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

    return ncenter

if __name__ == "__main__":
    G = nx.random_geometric_graph(500, 0.1)
    print(G.nodes)
    draw_graph(G)

    G_c = G
    print(G_c.nodes)
    G2 = cont_all_cliques_iterative(G_c, 5)
    ncenter = draw_graph(G2)

    G_c = G
    print(G_c.nodes)
    G3 = cont_all_cliques(G_c, 3)
    draw_graph(G3)

    G_c = G
    print(G_c.nodes)
    G4 = cont_all_stars_iterative(G_c, 20)
    draw_graph(G4)
