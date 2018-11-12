import matplotlib.pyplot as plt
import networkx as nx
import random

class Merger(object):

    def __init__(self, G):
        self.graph = G
        self.s_node = {}
        for node in G.nodes:
            self.s_node[node] = 30

    @staticmethod
    def random_color():
        """selecting random color in hex"""
        hex_digits = [0,0,0,0,0,0]
        for i in range(len(hex_digits)):
            hex_digits[i] = random.randint(0,15)
        result = "#"
        for dig in hex_digits:
            result = result + hex(dig).split('x')[-1]
        if result == "#000000" or result == "#FFFFFF":
            result = Merger.random_color()
        return result

    @staticmethod
    def color_cliques(G, min_node_num=3):
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
                clique_color = Merger.random_color()
                for node in clique:
                    p[node] = clique_color
                for node in clique:
                    for clique in cliques:
                        if node in clique:
                            cliques.remove(clique)
        return p

    def color_neighbors(self):
        """possibility of robustness loss"""
        p = {}
        for node in G:
            p[node] = "#000000"
        neighbor = {}

        for node in self.graph:
            neighbor[node] = list(nx.all_neighbors(self.graph, node))
        for value in neighbor:
            if int(len(neighbor[value])) > 10:
                color = Merger.random_color()
                p[value] = color
                for node in nx.all_neighbors(self.graph, value):
                    p[node] = color
            else :
                p[value] = 'grey'
        return p

    def cont_all_cliques_iterative(self, min_clique_node=4, node_size=30):
        for node in self.graph:
            self.s_node[node] = node_size
        cliques = list(nx.algorithms.find_cliques(self.graph))
        cliques.sort(key=len, reverse=True)
        while len(cliques[0]) > min_clique_node:
            clique = cliques[0]
            self.graph = self.contract_clique(clique)
            cliques = list(nx.algorithms.find_cliques(self.graph))
            cliques.sort(key=len, reverse=True)
        return self.graph

    def cont_all_cliques(self, min_clique_node=4):
        self.graph = self.graph
        cliques = list(nx.algorithms.find_cliques(self.graph))
        cliques.sort(key=len, reverse=True)
        while len(cliques[0]) >= min_clique_node:
            clique = cliques[0]
            for node in clique:
                for c in cliques:
                    if node in c and c != clique:
                        c.remove(node)
                        # print(node, "\t", c)
                        # cliques.remove(c)
            self.graph = self.contract_clique(clique)
            print(clique == cliques[0])
            cliques.remove(cliques[0])
            cliques.sort(key=len, reverse=True)
        return self.graph

    def contract_clique(self, clique):
        rand = random.randint(0, len(clique)-1)
        center = clique[0]
        clique.remove(center)
        for node in clique:
            # print(center, node)
            if node == center:
                continue
            try:
                self.graph = nx.contracted_nodes(self.graph, center, node, self_loops=False)
                self.s_node[center] += self.s_node[node]
            except nx.exception.NetworkXError as e:
                print("error: ", e)
                print(center, node)
        return self.graph

    def cont_all_stars_iterative(self, min_neighbors=10):
        neighbor = {}
        for node in self.graph:
            try:
                neighbors = list(nx.all_neighbors(self.graph, node))
            except nx.exception.NetworkXError:
                continue
            if len(neighbors) > min_neighbors:
                neighbor[node] = neighbors
                self.graph = self.contract_star(node)
                self.graph = nx.convert_node_labels_to_integers(self.graph)
        return self.graph

    def contract_star(self, center):
        result = self.graph
        for node in nx.all_neighbors(self.graph, center):
            result = nx.contracted_nodes(result, center, node)
        return result

    @staticmethod
    def draw_graph(G, node_size_dict=[]):
        print("# of edges:", G.number_of_edges())
        print("# of nodes:", G.number_of_nodes())
        # position is stored as node attribute data for random_geometric_graph
        pos = nx.get_node_attributes(G, 'pos')
        print(pos)
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

        p = Merger.color_cliques(G)

        if node_size_dict == []:
            node_size_dict = 30
        plt.figure(1,figsize=(8, 8))
        plt.subplot()
        nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.5)
        nx.draw_networkx_nodes(G, pos, nodelist=list(p.keys()),
                               node_size=node_size_dict,
                               node_color=list(p.values()),
                               cmap=plt.cm.Reds_r)
        # nx.draw_networkx(G,pos)
        plt.xlim(-0.05, 1.05)
        plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()

        return ncenter


if __name__ == "__main__":
    # G = nx.random_geometric_graph(1000, 0.08)
    # print(G.nodes)
    # Merger.draw_graph(G)
    #
    # G_c = G
    # print(G_c.nodes)
    # G2 = Merger(G)
    # G2.graph = G2.cont_all_cliques_iterative(7)
    # ncenter = Merger.draw_graph(G2.graph, node_size_dict=list(G2.s_node.values()))
    #
    # G_c = G
    # print(G_c.nodes)
    # G3 = Merger(G)
    # G3.graph = G3.cont_all_cliques(3)
    # Merger.draw_graph(G3)
    #
    # G_c = G
    # print(G_c.nodes)
    # G4 = Merger(G)
    # G4.graph = G4.cont_all_stars_iterative(20)
    # Merger.draw_graph(G4)
    G = nx.Graph()
    for i in range(8):
        G.add_node(i)
    for i in range(5):
        for j in range(5):
            if i != j:
                G.add_edge(i,j)
    for k in range(4):
        for l in range(4):
            if k != l:
                G.add_edge(k+4,l+4)
    print(G.nodes)
    print(G.edges)
    plt.figure(1, figsize=(8, 8))
    plt.subplot()
    nx.draw(G)
    plt.show()
    my_graph = Merger(G)
    my_graph.cont_all_cliques()