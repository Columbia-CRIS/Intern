from queue import Queue
from classes.graph import Graph
from functools import reduce
import networkx as nx
import numpy as np

# Calculates G, or the survival fitness function, for a given graph g
# Input: A graph
# Output: A fitness score
def evaluate(g, alpha):
    normEff = efficiency(g)
    normRob = robustness(g)
    return alpha * normEff + (1 - alpha) * normRob


# Calculates the efficiency of the graph by analyzing distances between every pair of
# nodes. Uses the NetworkX average_shortest_path_length function.
# Note: if an invalid graph is given, it returns -1
# Input: A graph
# Output: The efficiency value
def nx_efficiency(g):
    if (g.n <= 1): # Graph with just one node have no efficiency
        return -1

    G = nx.from_numpy_matrix(np.matrix(g.adj))
    APSP = nx.average_shortest_path_length(G)

    return 1 / APSP

# Calculates the efficiency of the graph by analyzing distances between every pair of
# nodes. This uses the Floyd Warshall algorithm.
# Note: if an invalid graph is given, it returns -1
# Input: A graph
# Output: The efficiency value
def efficiency(g):
    if (g.n <= 1): # Graph with just one node have no efficiency
        return -1

    # Find the distance for every pair of nodes
    dist = [[0 for c in range(g.n)] for r in range(g.n)]
    INF = 999

    # Set missing edges to infinity
    for r in range(g.n):
        for c in range(g.n):
            dist[r][c] = g.adj[r][c]
            if r != c and g.adj[r][c] == 0: # No edge exists between r and c
                dist[r][c] = INF

    # Floyd Warshall
    for k in range(g.n):
        for i in range(g.n):
            for j in range(g.n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    # Reset edges that are infinity
    for r in range(g.n):
        for c in range(g.n):
            if dist[r][c] == INF:
                dist[r][c] = 0

    # Calculation for average APSP for the given graph
    APSP = 0
    for r in dist:
        APSP += reduce(lambda x, y: x + y, r)
    APSP /= g.n * (g.n - 1)

    # APSP for a star
    starAPSP = 2 * (1 - 1 / g.n)

    # SECON metric
    # return starAPSP / APSP

    # New metric
    return 1 / APSP

# Calculates the structural and functional robustness of a graph
# Input: A graph
# Output: The robustness value
def robustness(g):
    strucR = [0] * g.n # Structural robustness with respect to each node
    # funcR = [0] * g.n # Functional robustness
    for j in range(g.n):
        modifiedAdj = []

        for r in range(g.n):
            if r != j: # Removing a node from the graph
                tmpArr = []
                for c in range(g.n):
                    if c != j:
                        tmpArr.append(g.adj[r][c])
                modifiedAdj.append(tmpArr)
        results = robustnessStack(modifiedAdj)

        # SECON metric
        strucR[j]  = results / (g.n - 2)

        # New metric: Number of neighbors
        # neighbors = 0
        # for r in range(g.n):
        #     if r != j and g.adj[j][r]:
        #         neighbors += 1
        # strucR[j]  = (results / (g.n - 2)) * neighbors / (g.e * 2)

    # SECON metric
    return min(strucR)

    # New metric
    # return sum(strucR)

# Calculates the structural of a graph using NetworkX functions
# Input: A graph
# Output: The robustness value
def nx_robustness(g):
    strucR = [0] * g.n # Structural robustness with respect to each node

    for j in range(g.n):
        modifiedAdj = []

        for r in range(g.n):
            if r != j: # Removing a node from the graph
                tmpArr = []
                for c in range(g.n):
                    if c != j:
                        tmpArr.append(g.adj[r][c])
                modifiedAdj.append(tmpArr)

        G = nx.from_numpy_matrix(np.matrix(modifiedAdj))
        numCC = nx.number_connected_components(G)
        effAccessibility = g.n - numCC - 1
        strucR[j]  = effAccessibility / (g.n - 2)

    return min(strucR)

# A robustness helper function that runs a DFS on the graph to populate a stack
# before running the individual functional and structural robustness calculations
# Input: An adjacency matrix
# Output: [functional robustness, structural robustness]
def robustnessStack(adj):
    visited = [False] * len(adj)
    stack = []

    for i in range(len(adj)):
        if visited[i] == False:
            dfsStackRecurse(adj, i, visited, stack)

    transposeAdj = transpose(adj)
    # return [functionalRobustness(transposeAdj, list(stack), adj),
    #         structuralRobustness(transposeAdj, list(stack))]
    return structuralRobustness(transposeAdj, stack)

# Calculates the functional robustness with respect to vertex j
# for a given graph (with vertex j removed, presumeably)
# TODO: Too inefficient time-wise (30x closer then structural calculation)
# Input: A transposed adjacency matrix of a graph, stack from DFS, original adjacency matrix
# Output: Functional robustness of the graph
def functionalRobustness(transposeAdj, stack, adj):
    visited = [False] * len(adj)
    largestSCC = []

    while len(stack) > 0:
        i = stack.pop()
        if visited[i] == False:
            tempSCC = dfsSCCRecurse(transposeAdj, i, visited)
            if len(tempSCC) > len(largestSCC):
                largestSCC = tempSCC

    # Create new graph with just the largest SCC
    newAdj = []
    newEdges = 0
    for i in largestSCC:
        tmpArr = []
        for j in largestSCC:
            if i == j:
                tmpArr.append(0)
            else:
                tmpArr.append(adj[i][j])
                newEdges += adj[i][j]
        newAdj.append(tmpArr)

    newG = Graph(len(newAdj), newEdges, True, False)
    newG.adj = newAdj
    return efficiency(newG)

# Calculates the effective accessibility of a graph.
# It does this by computing two DFS using Kosaraju's algorithm
# Input: A transposed adjacency matrix for a graph, stack from DFS
# Output: The effective accessibility of the graph
def structuralRobustness(transposeAdj, stack):
    visited = [False] * len(transposeAdj)
    accessibility = 0

    while len(stack) > 0:
        i = stack.pop()
        if visited[i] == False:
            accessibility += len(dfsSCCRecurse(transposeAdj, i, visited)) - 1
    return accessibility

# Runs a DFS of the graph and populates a stack with deepest nodes first
# Input: Adjacency matrix, node, boolean array of visited values, stack
# Output: Nothing
def dfsStackRecurse(adj, i, visited, stack):
    visited[i] = True
    for j in range(len(adj[i])):
        if adj[i][j] == 1 and visited[j] == False:
            dfsStackRecurse(adj, j, visited, stack)
    stack = stack.append(i)

# Runs a DFS on a graph and sums up the number of nodes of the strongly
# connected component (SCC) that contains node i
# Input: Adjacency matrix, node, boolean array of visited values
# Output: Nodes in the respective SCC (array)
def dfsSCCRecurse(adj, i, visited):
    visited[i] = True
    components = [i]
    for j in range(len(adj[i])):
        if adj[i][j] == 1 and visited[j] == False:
            components += dfsSCCRecurse(adj, j, visited)
    return components

# Check if a graph is connected. Uses Kosaraju algorithm for BFS.
# Input: Adjacency matrix
# Output: Boolean
def isConnected(adj):
    if len(adj) == 0:
        return True

    if not bfs(adj):
        return False

    transposeAdj = transpose(adj)
    return bfs(transposeAdj)


# Breadth first search that always starts with node 0
# Input: Adjacency matrix
# Output: Boolean for if it visited every node from 0 via BFS
def bfs(adj):
    if len(adj) == 0:
        return true

    explored = [0] * len(adj)
    q = Queue(len(adj) ** 2)
    q.put_nowait(0)

    while not q.empty():
        n = q.get_nowait() # Visit node
        if explored[n] == 0:
            explored[n] = 1
            # Find neighbors
            for neighbor in range(len(adj[n])):
                if adj[n][neighbor] > 0:
                    q.put(neighbor)

    for nodeState in explored:
        if nodeState == 0:
            return False
    return True

# Transpose an adjacency matrix
# Input: Adjacency matrix
# Output: Tranposed adjacency matrix
def transpose(adj):
    return [[adj[j][i] for j in range(len(adj))] for i in range(len(adj[0]))]
