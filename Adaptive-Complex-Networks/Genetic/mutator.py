from random import randint
from evaluator import isConnected
from copy import deepcopy
from classes.graph import Graph

# Mutates a pool of candidate graphs with their fitness score.
# Picks the best 2, reproduces them, and then mutate their children
# Input: Pool of parents, respective array of fitness scores, connectedness, directedness
# Output: Pool of children (same size as parents)
def mutate(pool, fitness, gensWithoutChange, connected, directed, annealing):
    # Indices for the best performing parents
    parent1 = 0
    parent2 = 1

    # Find the best two parents
    for i in range(2, len(fitness)):
        if fitness[i] > fitness[parent1]:
            parent2 = parent1
            parent1 = i
        elif fitness[i] > fitness[parent2]:
            parent2 = i

    # Reproduction
    if annealing:
        children = [None] * len(pool)
    else:
        children = [None] * (len(pool) - 1)


    if annealing:
        print("Running annealing")

    for i in range(len(children)):
        if annealing:
            # Sexual mutation
            p1 = randint(0, len(pool) - 1)
            p2 = randint(0, len(pool) - 1)
            while p2 == p1:
                p2 = randint(0, len(pool) - 1)
            children[i] = crossover(pool[p1], pool[p2], directed)
        else:
            children[i] = crossover(pool[parent1], pool[parent2], directed)
        # Asexual mutation
        mutateEdge(children[i], pool[parent1].e, directed, connected)
        while connected and not isConnected(children[i].adj):
            mutateEdge(children[i], pool[parent1].e, directed, connected)
    if not annealing:
        children.append(pool[parent1]) # Add the best parent back into children
    return children

# Asexually mutates a graph with respect to its edges. It checks if the graph has
# the correct number of edges and does mutations either to revert it to the correct
# number of edges, or just randomly moves edges around.
# Input: Adjacency matrix, correct number of edges, directedness
# Output: Nothing
def mutateEdge(g, edges, directed, connected):
    """ Asexually mutates a graph with respect to its edges. 
        Checks whether the graph has the correct number of 
        edges and does mutations to revert it to the correct 
        number of edges, or just randomly moves edges around. 

        Input: Adjacency Matrix, correct number of edges, directedness
<<<<<<< HEAD
        
=======
>>>>>>> c8a89229c50067ebeb60c26d2f4fa1d4efe9bc61
        Makes changes directly to Matrix (no output)
    """
    if ((directed and g.e == g.n ** 2 - g.n)
        or (not directed and g.e == (g.n ** 2 - g.n) / 2)): # Complete graph
        return

    if (g.e > edges):
        while g.e != edges:
            removeEdge(g, directed)
            g.e -= 1
    elif (g.e < edges):
        while g.e != edges:
            addEdge(g, directed, connected)
            g.e += 1
    else: # Edge count is correct, just do an edge swap for the mutation
        removeEdge(g, directed)
        addEdge(g, directed, connected)

# Removes an edge from a graph
# Input: A graph, directedness
# Output: Nothing
def removeEdge(g, directed):
    edge = randint(1, g.e) # Randomly chosen edge to remove
    removeCounter = 0 # Count up to the number "edge"'

    for r in range(g.n):
        for c in range(g.n):
            if directed and g.adj[r][c] > 0:
                removeCounter += 1

                if removeCounter == edge: # Remove the edge once we reach "edge"
                    g.adj[r][c] = 0
                    return
            elif not directed and r < c and g.adj[r][c] > 0:
                removeCounter += 1

                if removeCounter == edge: # Remove the edge once we reach "edge"
                    g.adj[r][c] = 0
                    g.adj[c][r] = 0
                    return

# Adds an edge to a graph
# Input: A graph, directedness
# Output: Edge index that was added
def addEdge(g, directed, connected):
    required = [] # Unconnected nodes
    for r in range(g.n):
        edgeSum = 0
        for c in range(g.n):
            edgeSum += g.adj[r][c]

        if edgeSum == 0:
            required.append(r)

    if len(required) == 0 or not connected: # No unconnected nodes, add edge anywhere
        empty = randint(1, g.n ** 2 - g.n - g.e) # Randomly chosen nonedge to add
        if not directed:
            empty = randint(1, (g.n ** 2 - g.n)/2 - g.e)
        addCounter = 0 # Count up to the number "empty"

        for r in range(g.n):
            for c in range(g.n):
                if directed and r != c and g.adj[r][c] == 0:
                    addCounter += 1

                    if addCounter == empty: # Add edge once we reach "empty"
                        g.adj[r][c] = 1
                        return empty
                elif not directed and r < c and g.adj[r][c] == 0:
                    addCounter += 1

                    if addCounter == empty: # Add edge once we reach "empty"
                        g.adj[r][c] = 1
                        g.adj[c][r] = 1
                        return empty
    else: # Has unconnected node, add edge to connect
        empty = randint(1, len(required) * (g.n - 1))
        addCounter = 0

        for r in required:
            for c in range(g.n):
                if directed and r != c:
                    addCounter += 1
                    if addCounter == empty:
                        g.adj[r][c] = 1
                        return
                elif not directed and r != c:
                    addCounter += 1
                    if addCounter == empty:
                        g.adj[r][c] = 1
                        g.adj[c][r] = 1
                        return

# Generating unbiased sub-rectangle dimensions
def generateRectangle(n):
    col1 = randint(0, n - 1)
    col2 = randint(0, n - 1)
    while col1 == col2: # Make sure col2 does not equal col1
        col2 = randint(0, n - 1)
    left = min(col1, col2)
    right = max(col1, col2)

    row1 = randint(0, n - 1)
    row2 = randint(0, n - 1)
    while row1 == row2: # Make sure row2 does not equal row1
        row2 = randint(0, n - 1)
    top = min(col1, col2)
    bottom = max(col1, col2)

    return {
        'left': left,
        'right': right,
        'top': top,
        'bottom': bottom,
    }

# Crossover sexual reproduction between 2 graphs. It randomly selects a subrectangle
# in g1 that will be replaced with g2's edges, and vise versa
# Input: Two graphs, directedness (boolean)
# Output: n children graphs
def crossover(g1, g2, directed):
    if g1.n != g2.n: # The dimensions of the graphs don't match
        raise AttributeError('Dimensions of graphs do not match')

    # Randomly pick which graph is the base to be added upon
    base = g2
    addendum = g1
    if (randint(0, 1) == 1):
        base = g1
        addendum = g2

    child = Graph(base.n, base.e, base.connected, base.weighted)
    childEdges = 0
    rect = generateRectangle(base.n)

    if directed: # Directed graph
        for r in range(base.n):
            for c in range(base.n):
                # If r, c indices not in the subrectangle
                if r < rect['top'] or r > rect['bottom'] or c < rect['left'] or c > rect['right']:
                    child.adj[r][c] = base.adj[r][c]
                else:
                    child.adj[r][c] = addendum.adj[r][c]

                if child.adj[r][c] == 1:
                    childEdges += 1
        child.e = childEdges # Properly update the edge count
    else: # Undirected graph
        # Generate a rectangle that contains elements in the upper right triangle
        while (rect['bottom'] < rect['right'] and rect['top'] < rect['left']):
            rect = generateRectangle(base.n)

        for r in range(base.n):
            for c in range(base.n):
                if c < r:
                    child.adj[r][c] = child.adj[c][r]
                elif c > r:
                    # If r, c indices not in the subrectangle
                    if r < rect['top'] or r > rect['bottom'] or c < rect['left'] or c > rect['right']:
                        child.adj[r][c] = base.adj[r][c]
                    else:
                        child.adj[r][c] = addendum.adj[r][c]

                    if child.adj[r][c] == 1:
                        childEdges += 1
        child.e = childEdges # Properly update the edge count

    return child
