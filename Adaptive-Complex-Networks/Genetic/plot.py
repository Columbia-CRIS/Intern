import evaluator
from classes.graph import Graph
import matplotlib.pyplot as plt
from copy import deepcopy

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
    if n % 2 == 0:
        half -= 1

    g = Graph(n, n, True, False)
    for i in range(g.n):
        # print(i)
        if i + 1 < half:
            g.adj[i][i+1] = 1
            g.adj[i+1][i] = 1
            g.adj[i][i + half] = 1
            g.adj[i + half][i] = 1
        elif i == half:
            g.adj[i][0] = 1
            g.adj[0][i] = 1
            g.adj[i][i + half] = 1
            g.adj[i + half][i] = 1

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

n = list(range(5, 51, 1))
obj = {}
for j in range(0, 11):
    alpha = j/10
    obj[alpha] = []
    for i in n:
        g = star(i)
        obj[alpha].append(evaluator.evaluate(g, alpha))

ax = plt.subplot(111)
ax.set_color_cycle(["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"])
for alpha in obj:
    ax.plot(n, obj[alpha], label=str(alpha))

handles, labels = ax.get_legend_handles_labels()
newHandles = []
newLabels = deepcopy(labels)
newLabels.sort(key=float)
for i in newLabels:
    newHandles.append(handles[labels.index(i)])

print(newLabels)

ax.legend(newHandles, newLabels, loc='lower left')
plt.xlabel('nodes')
plt.ylabel('score')
plt.xlim(-10,50)
plt.title('Star Graph')
plt.show()
