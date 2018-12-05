import matplotlib.pyplot as plt
import networkx as nx
import random
from sklearn.externals import joblib
import os
import evaluator
import numpy as np
import graph
import math
from numpy import linspace


class Merger(object):

    def __init__(self, G):
        self.graph = G
        self.s_node = {}
        for node in G.nodes:
            self.s_node[node] = 30
        self.level = [self.graph]
        nx.set_node_attributes(self.graph, self.s_node, name="node_size_concat")
        self.min_coloring = 3
        self.node_tree = {}
        for node in G.nodes:
            self.node_tree[node] = [node]
        self.node_tree_level = []
        self.node_tree_level.append(self.node_tree)

    @staticmethod
    def random_color():
        """selecting random color in hex"""
        hex_digits = [0, 0, 0, 0, 0, 0]
        for i in range(len(hex_digits)):
            hex_digits[i] = random.randint(0, 15)
        result = "#"
        for dig in hex_digits:
            result = result + hex(dig).split('x')[-1]
        if result == "#000000" or result == "#FFFFFF":
            result = Merger.random_color()
        return result

    @staticmethod
    def color_cliques(G, min_node_num=4):
        """hubs(cliques) are complete subgraphs of G"""
        p_list = list(G.nodes)
        p = {}
        for thing in p_list:
            p[thing] = "#000000"

        cliques = list(nx.algorithms.find_cliques(G))
        # order cliques in descending order depending on size
        for clique in cliques:
            clique.sort()
        cliques.sort()
        cliques.sort(key=len, reverse=True)

        for clique in cliques:
            if len(clique) >= min_node_num:
                clique_color = Merger.random_color()
                for node in clique:
                    p[node] = clique_color
                for node2 in clique:
                    for clique2 in cliques:
                        if node2 in clique2 and clique != clique2:
                            clique2.remove(node2)
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
            else:
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
        for clique in cliques:
            clique.sort()
        cliques.sort()
        cliques.sort(key=len, reverse=True)
        # print(cliques)
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
        self.node_tree_level.append(self.node_tree)
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
        cont_nodes = []
        for node in clique:
            # print(center, node)
            if node == center:
                continue
            try:
                self.graph = nx.contracted_nodes(self.graph, center, node, self_loops=False)
                self.s_node[center] += self.s_node[node]
                cont_nodes.append(node)
            except nx.exception.NetworkXError:
                pass  # print("error: ", e)
                # print(center, node)
        self.node_tree[center].append(cont_nodes)
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

        plt.figure(1, figsize=(8, 8))
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
            degree = len(list(nx.neighbors(G, node)))
            degree_list.append(degree)
            try:
                degree_dict[degree] += 1
            except KeyError:
                degree_dict[degree] = 1
        bin = Merger.get_bins(degree_list)
        plt.hist(degree_list, bins=bin)
        if log_scale:
            plt.semilogy()
            plt.semilogx()
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
        result_bin = Merger.get_bins(flattened_list)
        plt.hist(flattened_list, bins=result_bin)
        if log_scale:
            plt.semilogy()
            plt.semilogx()
        plt.xlabel('# shortest path length')
        plt.ylabel('# connections')
        plt.title('spd_dist')
        plt.show()
        return shortest_path_dict

    @staticmethod
    def get_bins(data):
        start = min(data) - 0.5
        end = max(data) + 0.5
        b_count = start
        result_bin = []
        while b_count <= end:
            result_bin.append(b_count)
            b_count += 1
        return result_bin

    def print_concat_nodes(self, level=-1):
        for key in self.node_tree_level[level].keys():
            if len(self.node_tree[key]) > 1:
                print(str(key) + ": " + str(self.node_tree[key]))


def graph_from_grpah(G):
    """Graph from networkx grpah"""
    g = graph.Graph(len(G.nodes), list(G.edges), False, False)
    return g


def robustness(G):
    rb = []
    tmp_g = nx.Graph(G)
    for node in tmp_g.nodes:
        tmp_g.remove_node(node)

        cc = nx.number_connected_components(tmp_g)
        num_nodes = len(list(tmp_g.nodes))
        effAccessibility = num_nodes - cc - 1
        rb.append(effAccessibility / (num_nodes - 2))

        tmp_g.add_node(node)

    return min(rb)


def robustness2(merger):
    return robustness(merger.graph)


def efficiency(merger):
    return nx.global_efficiency(merger.graph)


def main_old():
    node_num = 100
    graph_float = 0.07
    G = nx.random_geometric_graph(node_num, graph_float)
    # G = nx.MultiGraph(G)
    print(nx.global_efficiency(G))
    print(robustness(G))
    # G = nx.MultiGraph(G)
    # print(G.nodes)
    Merger.draw_graph(G)

    degree_log = True
    spd_log = False

    # print(Merger.plot_degree(G, degree_log))
    # print(Merger.plot_spd(G, spd_log))

    G3 = Merger(G)
    G3.graph = G3.cont_all_cliques(4)
    print(nx.global_efficiency(G3.graph))
    print(robustness(G3.graph))

    Merger.draw_graph(G3.graph, node_size_dict=G3.s_node, label=False)
    # print(Merger.plot_degree(G3.graph, degree_log))
    # print(Merger.plot_spd(G3.graph, spd_log))
    G3.graph = G3.cont_all_cliques(4)
    print(nx.global_efficiency(G3.graph))
    print(robustness(G3.graph))
    Merger.draw_graph(G3.graph, node_size_dict=G3.s_node, label=False)
    # print(Merger.plot_degree(G3.graph, degree_log))
    # print(Merger.plot_spd(G3.graph, spd_log))
    G3.graph = G3.cont_all_cliques(4)
    print(nx.global_efficiency(G3.graph))
    print(robustness(G3.graph))
    Merger.draw_graph(G3.graph, node_size_dict=G3.s_node, label=False)
    # print(Merger.plot_degree(G3.graph, degree_log))
    # print(Merger.plot_spd(G3.graph, spd_log))

    file_name = str(node_num) + "_" + str(graph_float)
    count = 1
    if file_name in os.listdir(os.path.curdir):
        file_name_tmp = str(node_num) + "_" + str(graph_float) + str(count)
        while file_name_tmp in os.listdir(os.path.curdir):
            count += 1
    file_name = file_name + str(count)

    uinput = input("Save the graph? y/n: ")
    if uinput == 'y':
        joblib.dump(G3, os.path.join(os.path.abspath(os.path.curdir), file_name))


def small_graph():
    G = nx.Graph()
    for i in range(8):
        G.add_node(i)
    for i in range(5):
        for j in range(5):
            if i != j:
                G.add_edge(i, j)
    for k in range(4):
        for l in range(4):
            if k != l:
                G.add_edge(k + 4, l + 4)
    print(G.nodes)
    print(G.edges)
    plt.figure(1, figsize=(8, 8))
    plt.subplot()
    nx.draw(G)
    plt.show()
    my_graph = Merger(G)
    my_graph.cont_all_cliques(min_clique_node=3)
    print(my_graph.graph.edges)
    plt.figure(2, figsize=(8, 8))
    plt.subplot()
    nx.draw(my_graph.graph, node_size_dict=30)
    plt.show()


def get_efficiency_list(M, steps=3):
    r = []
    tmp = Merger(M.graph)
    for i in range(steps):
        r.append(efficiency(tmp))
        tmp.cont_all_cliques()
    return r


def get_robustness_list(M, steps=3):
    r = []
    tmp = Merger(M.graph)
    for i in range(steps):
        r.append(robustness2(tmp))
        tmp.cont_all_cliques()
    return r


# for multiprocessing
def a_e_l(i, M, e_d, steps=3):
    e_d[i] = get_efficiency_list(M, steps)
    print(e_d, "done!")


# for multiprocessing
def a_r_l(i, M, r_d, steps=3):
    r_d[i] = get_robustness_list(M, steps)
    print(r_d, "donezoed!")


if __name__ == "__main__":
    from multiprocessing import Process
    import multiprocessing

    manager = multiprocessing.Manager()
    e_dict = manager.dict()
    r_dict = manager.dict()

    graphs = []
    for i in range(20):
        y_f = 0.05992949 + (258735.2 - 0.05992949) / (1 + (((i + 1) * 100) / 3.673678e-10) ** 0.5484871)
        tmp_g = nx.random_geometric_graph((i + 1) * 100, y_f)
        tmp_g = Merger(tmp_g)
        graphs.append(tmp_g)

    for j in range(20):
        pe = Process(target=a_e_l, args=(j, graphs[j], e_dict))
        pe.start()

    for m in range(20):
        p = Process(target=a_r_l, args=(m, graphs[m], r_dict))
        p.start()

    p.join()
    r_list = list(r_dict.values())

    u = linspace(0, 3, 3)
    for l in range(20):
        plt.plot(u, r_list[l], Merger.random_color())
    plt.show()

    pe.join()
    e_list = list(e_dict.values())
    t = linspace(0, 3, 3)
    for k in range(20):
        plt.plot(t, e_list[k], Merger.random_color())
    plt.show()

    """
    graphs = []
    for i in range(10):
        tmp_g = nx.random_geometric_graph(1000, 0.07)
        tmp_g = Merger(tmp_g)
        graphs.append(tmp_g)
    for k in range(3):
        e = sorted(graphs, key=efficiency)
        r = sorted(graphs, key=robustness2)
        print("efficiency: {} robustness: {}".format(e, r))
        for j in range(len(graphs)):
            tmp = graphs[j]
            tmp.cont_all_cliques()
            graphs[j] = tmp
    """
