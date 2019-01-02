import argparse

from iterator import iterate, saveGraph
import evaluator
import networkx as nx
import numpy as np
import matplotlib.pyplot as savefig
import matplotlib.pyplot as plt

# Takes the user input and checks for invalidity
# Input: Args object
# Output: The best graph given by GA
def initialize(args):
    """ Initializes the program and checks for user input validity """
    if (args.a > 1 or args.a < 0):
        raise ValueError('Alpha value is not between 0 and 1')
    elif (args.p < 2):
        raise ValueError('Parent pool size must be at least 2')
    elif (args.n < 2):
        raise ValueError('Number of nodes must be at least 2')
    elif (args.e < 1):
        raise ValueError('Number of edges must be at least 1')

    return iterate(args) # calls iterate function in iterator.py

def show_graph_with_labels(adjacency_matrix):
    """ Creates a graph from a given adjacency matrix """
    gr = nx.from_numpy_matrix(np.matrix(adjacency_matrix))
    nx.draw(gr)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''A genetic algorithm that generates network topologies based on user input''')
    parser.add_argument('--n', type=int, default=10, help='The number of nodes in the network: [2, INF)')
    parser.add_argument('--e', type=int, default=30, help='The number of edges in the network: [1, INF)')
    parser.add_argument('--z', type=bool, default=False, help='Edge count can evolve & change stay btw generations (default: false)')
    parser.add_argument('--p', type=int, default=10, help='Parent pool size for the GA: [2, INF)')
    parser.add_argument('--s', type=int, default=250, help='Number of generations without improvement before stopping')
    parser.add_argument('--a', type=float, default=0, help='Alpha value for evaluation: [0, 1]')
    parser.add_argument('--c', type=bool, default=True, help='Whether the graph should be connected (default: true)')
    parser.add_argument('--w', type=bool, default=False, help='Whether the graph should be weighted (default: false) [TODO]')
    parser.add_argument('--d', type=bool, default=False, help='Whether the graph should be directed (default: false)')
    parser.add_argument('--v', type=bool, default=False, help='Verbose logging (default: false)')

    best = initialize(parser.parse_args()) # calls initialize function from above
    print("efficiency", evaluator.nx_efficiency(best))
    print("robustness", evaluator.nx_most_connected_robustness(best))
    print("redundancy", evaluator.redundancy(best))
    print("edges", best.e)
    print("nodes", best.n)
    if best.n <= 20: # This way logging does not take over whole screen
        show_graph_with_labels(best.adj)
    saveGraph(best.adj, 'BEST')
    print(best)
