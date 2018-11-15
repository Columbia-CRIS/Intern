import matplotlib.pyplot as plt
import networkx as nx
import random
import numpy as np



class Merger(object):

    def __init__(self, G):
        self.graph = G
        self.s_node = {}
        for node in G.nodes:
            self.s_node[node] = 30
        self.level = [self.graph]
        nx.set_node_attributes(self.graph, self.s_node, name="node_size_concat")
        self.min_coloring = 3

    @staticmethod
    def random_color():
        """selecting random color in hex"""
        hex_digits = [0, 0, 0, 0, 0, 0]
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

        cliques = list(nx.algorithms.find_cliques(G))
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
                    for clique2 in cliques:
                        if node in clique2:
                            cliques.remove(clique2)
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
        cliques = list(nx.algorithms.find_cliques(self.graph))
        cliques.sort(key=len, reverse=True)
        while len(cliques) > 0 and len(cliques[0]) >= min_clique_node:
            clique = cliques[0]
            # print(clique)
            for node in clique:
                for c in cliques:
                    if node in c and c != clique:
                        c.remove(node)
                        # print(node, "\t", c)
                        # cliques.remove(c)
            self.graph = self.contract_clique(clique)
            cliques.remove(cliques[0])
            cliques.sort(key=len, reverse=True)
            # print(cliques)
        self.level.append(self.graph)
        return self.graph

    def contract_clique(self, clique):
        def get_biggest_node(m, cur_clique):
            max_size_node = cur_clique[0]
            for node in cur_clique:
                if m.s_node[node] > m.s_node[max_size_node]:
                    max_size_node = node
            return max_size_node

        center = get_biggest_node(self, clique)
        # x_sum = 0
        # y_sum = 0
        # pos = nx.get_node_attributes(self.graph, "pos")
        # for node in clique:
        #     try:
        #         x_sum += pos[node][0]
        #         y_sum += pos[node][1]
        #     except:
        #         pass
        # new_node_x = x_sum/len(clique)
        # new_node_y = y_sum/len(clique)
        # pos[center] = [new_node_x, new_node_y]
        # nx.set_node_attributes(G, pos, "pos")
        clique.remove(center)
        for node in clique:
            # print(center, node)
            if node == center:
                continue
            try:
                self.graph = nx.contracted_nodes(self.graph, center, node, self_loops=False)
                self.s_node[center] += self.s_node[node]
            except nx.exception.NetworkXError as e:
                pass # print("error: ", e)
                # print(center, node)
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
    def draw_graph(G, node_size_dict={}, label=False):
        """this is specific to the graph with positions"""
        print("# of edges:", G.number_of_edges())
        print("# of nodes:", G.number_of_nodes())
        # position is stored as node attribute data for random_geometric_graph
        pos = nx.get_node_attributes(G, 'pos')
        # print(pos)
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

        if node_size_dict == {}:
            for node in G.nodes:
                node_size_dict[node] = 30

        node_size_list = []
        for node in G.nodes:
            node_size_list.append(node_size_dict[node])

        plt.figure(1,figsize=(8, 8))
        plt.subplot()
        nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.5)
        nx.draw_networkx_nodes(G, pos, nodelist=G.nodes,
                               node_size=node_size_list,
                               node_color=list(p.values()),
                               cmap=plt.cm.Reds_r)
        if label:
            nx.draw_networkx_labels(G, pos)
        # nx.draw_networkx(G,pos)
        plt.xlim(-0.05, 1.05)
        plt.ylim(-0.05, 1.05)
        plt.axis('off')
        plt.show()

        return ncenter

    @staticmethod
    def plot_degree(G, log_scale=True):
        degree_dict = {}
        degree_list = []
        for node in G.nodes:
            degree = len(list(nx.neighbors(G,node)))
            degree_list.append(degree)
            try:
                degree_dict[degree] += 1
            except KeyError:
                degree_dict[degree] = 1
        bin = Merger.get_bins(degree_list)
        plt.hist(degree_list, bins=bin)
        if log_scale:
            plt.semilogy()
        plt.xlabel('degree')
        plt.ylabel('# nodes')
        plt.title('degree_dist')
        plt.show()
        return degree_dict

    @staticmethod
    def plot_spd(G, log_scale=False):
        spd = nx.shortest_path_length(G)
        # print(list(spd))
        shortest_path_dict = {}
        shortest_paths = []
        for node in spd:
            shortest_paths.append(list(node[1].values()))
            for length in node[1].values():
                try:
                    shortest_path_dict[length] += 1
                except KeyError:
                    shortest_path_dict[length] = 1
        flattened_list = [y for x in shortest_paths for y in x]
        bin = Merger.get_bins(flattened_list)
        plt.hist(flattened_list,bins=bin)
        if log_scale:
            plt.semilogy()
        plt.xlabel('# shortest path length')
        plt.ylabel('# connections')
        plt.title('spd_dist')
        plt.show()
        return shortest_path_dict

    @staticmethod
    def get_bins(data):
        start = min(data)-0.5
        end = max(data)+0.5
        count = start
        bin = []
        while count <= end:
            bin.append(count)
            count+=1
        return bin


if __name__ == "__main__":
    G = nx.random_geometric_graph(10000, 0.021)
    # G = nx.MultiGraph(G)
    # print(G.nodes)
    Merger.draw_graph(G)


    degree_log = True
    spd_log = False

    print(Merger.plot_degree(G, degree_log))
    print(Merger.plot_spd(G, spd_log))

    G3 = Merger(G)
    G3.graph = G3.cont_all_cliques(4)
    Merger.draw_graph(G3.graph, node_size_dict=G3.s_node)
    print(Merger.plot_degree(G3.graph, degree_log))
    print(Merger.plot_spd(G3.graph, spd_log))
    G3.graph = G3.cont_all_cliques(4)
    Merger.draw_graph(G3.graph, node_size_dict=G3.s_node)
    print(Merger.plot_degree(G3.graph, degree_log))
    print(Merger.plot_spd(G3.graph, spd_log))
    G3.graph = G3.cont_all_cliques(4)
    Merger.draw_graph(G3.graph, node_size_dict=G3.s_node)
    print(Merger.plot_degree(G3.graph, degree_log))
    print(Merger.plot_spd(G3.graph, spd_log))

    """testing with small graph discussed"""
    # G = nx.Graph()
    # for i in range(8):
    #     G.add_node(i)
    # for i in range(5):
    #     for j in range(5):
    #         if i != j:
    #             G.add_edge(i,j)
    # for k in range(4):
    #     for l in range(4):
    #         if k != l:
    #             G.add_edge(k+4,l+4)
    # print(G.nodes)
    # print(G.edges)
    # plt.figure(1, figsize=(8, 8))
    # plt.subplot()
    # nx.draw(G)
    # plt.show()
    # my_graph = Merger(G)
    # my_graph.cont_all_cliques(min_clique_node=3)
    # print(my_graph.graph.edges)
    # plt.figure(2, figsize=(8, 8))
    # plt.subplot()
    # nx.draw(my_graph.graph, node_size_dict=30)
    # plt.show()
