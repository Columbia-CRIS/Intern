class Graph:
    def __init__(self, n, e, connected, weighted):
        self.n = n # Nodes
        self.e = e # Edges
        self.connected = connected # Connected? [TODO: Remove]
        self.weighted = weighted # Weighted? [TODO: Remove]
        self.adj = [[0 for i in range(n)] for j in range(n)] # creates adjacency matrix populated with all 0s
        # adjacency matrix: matrix with "1" noting if two nodes i, j are connected and "0" if not
    def __str__(self):
        printStr = "   "
        for i in range(self.n):
            printStr += str(i) + ", "
        printStr += "\n"
        for i in range(self.n):
            printStr += str(i) + " " + str(self.adj[i]) + "\n"
        return printStr
    def resetEdges(self):
        self.adj = [[0 for i in range(self.n)] for j in range(self.n)]
