import iterator
import evaluator
import mutator
import generator
# import os
from classes.graph import Graph
from copy import deepcopy
import networkx as nx
import numpy as np
import matplotlib.pyplot as savefig
import matplotlib.pyplot as plt
import time

def show_graph_with_labels(adjacency_matrix):
    gr = nx.from_numpy_matrix(np.matrix(adjacency_matrix))
    nx.draw(gr)
    plt.show()

def pent(n): # Pentahub
    g = Graph(n, n, True, False)
    first = int(n/5)
    second = int(2 * n/5)
    third = int(3 * n/5)
    fourth = int(4 * n/5)
    fifth = n

    for i in range(g.n):
        if i != 0 and i < first:
            g.adj[i][0] = 1
            g.adj[0][i] = 1
        elif i != first and i < second:
            g.adj[i][first] = 1
            g.adj[first][i] = 1
        elif i != second and i < third:
            g.adj[i][second] = 1
            g.adj[second][i] = 1
        elif i != third and i < fourth:
            g.adj[i][third] = 1
            g.adj[third][i] = 1
        elif i != fourth and i < fifth:
            g.adj[i][fourth] = 1
            g.adj[fourth][i] = 1

        g.adj[0][first] = 1
        g.adj[first][0] = 1

        g.adj[first][second] = 1
        g.adj[second][first] = 1

        g.adj[second][third] = 1
        g.adj[third][second] = 1

        g.adj[third][fourth] = 1
        g.adj[fourth][third] = 1

        g.adj[fourth][0] = 1
        g.adj[0][fourth] = 1

    return g

def tri(n): # TriHub
    g = Graph(n, n, True, False)
    first = int(n/3)
    second = int(2 * n/3)
    third = n

    for i in range(g.n):
        if i != 0 and i < first:
            g.adj[i][0] = 1
            g.adj[0][i] = 1
        elif i != first and i < second:
            g.adj[i][first] = 1
            g.adj[first][i] = 1
        elif i != second and i < third:
            g.adj[i][second] = 1
            g.adj[second][i] = 1

        g.adj[0][first] = 1
        g.adj[first][0] = 1

        g.adj[first][second] = 1
        g.adj[second][first] = 1

        g.adj[second][0] = 1
        g.adj[0][second] = 1

    return g

def perfect(n):
    half = int(n/2)
    # if n % 2 == 0:
    #     half -= 1

    g = Graph(n, n, True, False)
    for i in range(half):
        g.adj[i][i + half] = 1
        g.adj[i + half][i] = 1


    g.adj[0][14] = 1
    g.adj[14][0] = 1
    for i in range(half):
        if i + 1< half:
            g.adj[i][i+1] = 1
            g.adj[i+1][i] = 1

            # g.adj[i][i + half] = 1
            # g.adj[i + half][i] = 1

    return g

def circle(n):
    g = Graph(n, n, True, False)
    for i in range(g.n):
        if i == g.n - 1:
            g.adj[i][0] = 1
            g.adj[0][i] = 1
        else:
            g.adj[i][i+1] = 1
            g.adj[i+1][i] = 1

    return g

def line(n):
    g = Graph(n, n - 1, True, False)
    for i in range(g.n):
        if i != g.n - 1:
            g.adj[i][i+1] = 1
            g.adj[i+1][i] = 1

    return g

def star(n):
    g = Graph(n, n-1, True, False)
    for i in range(1, g.n):
        g.adj[i][0] = 1
        g.adj[0][i] = 1
    return g

# g = star(30)
# for r in range(g.n):
    # neighbors = 0
    # for c in range(g.n):
    #     if r < c and g.adj[r][c]:
    #         neighbors += 1
    # print("Neigbors", neighbors)

# g = Graph(30, 29, True, False)
# for i in range(g.n):
#     if i < 5:
#         g.adj[i][29] = 1
#         g.adj[29][i] = 1
#     elif i < 29:
#         g.adj[i][i % 5] = 1
#         g.adj[i % 5][i] = 1
    # elif i == 27 or i == 28:
    #     g.adj[i][29] = 1
    #     g.adj[29][i] = 1


### NetworkX is a lot faster for efficiency
# g = perfect(30)
# start = time.time()
# print("Eff", evaluator.efficiency(g))
# end = time.time()
# print(end - start)
#
# start = time.time()
# print("Nx Eff", evaluator.nx_efficiency(g))
# end = time.time()
# print(end - start)

### NetworkX is a lot slower for robustness
g = pent(30)
start = time.time()
print("Rob", evaluator.robustness(g))
end = time.time()
print(end - start)

start = time.time()
print("Nx Rob", evaluator.nx_robustness(g))
end = time.time()
print(end - start)


# show_graph_with_labels(g.adj)
# he = '/Users/Jackson/Documents/School/research/genetic/img/'
# for filename in os.listdir('/Users/Jackson/Documents/School/research/genetic/img'):
#     lol = filename.split('.')
#     if lol[0] != '' and int(lol[0]) >= 10 and int(lol[0]) < 100:
#         os.rename(he + filename, he + '0' + filename)
