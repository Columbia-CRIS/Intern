import os
import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
from Evaluator import evaluator
import collections

# print(os.getcwd())

path_to_data = "/Users/abhishek/Documents/Complexity-and-Emergence"

# filename = path_to_data+"/Datasets/bio-celegans-dir/bio-celegans-dir.edges"
# filename = path_to_data+"/Datasets/bio-grid-fruitfly/bio-grid-fruitfly.edges"
filename = path_to_data+"/Datasets/bio-celegans/bio-celegans.mtx"
filename = path_to_data+"/Datasets/bio-Wormnet-v3-benchmark/bio-Wormnet-v3-benchmark.edges"

fopen = open(filename,'rb')
fopen = filename

# Various read strategies

#Strategy 1
G = nx.read_edgelist(fopen)  # For celegans-dir, Wormnet-benchmark


# with open(filename, 'rb') as f:
#     ncols = len(next(f).split('\t'))
#
# x = np.genfromtxt(filename, delimiter='\t', dtype=None, names=True,
#                   usecols=range(1,ncols) # skip the first column
#                   )
# labels = x.dtype.names
#
# # y is a view of x, so it will not require much additional memory
# y = x.view(dtype=('int', len(x.dtype)))
#
# G = nx.from_numpy_matrix(y)
# G = nx.relabel_nodes(G, dict(zip(range(ncols-1), labels)))


Gn = G.nodes()
Ge = G.edges(data = True)

A = nx.to_numpy_matrix(G, weight = 'weight')

Asymtest = A+np.transpose(A) - 2*A
N = len(Gn)
E = len(Ge)
print("Number of nodes in the graph : ", N)
print("Number of edges in the graph : ", E)

is0 = 0
Asymtest = np.asmatrix(Asymtest)
for row in range(N):
    for col in range(N):
        is0 = is0+Asymtest[row,col]

if is0==0:
    print("Matrix is symmetric")


## Network metrics evaluation

R1 = evaluator.Entropy_imp(A)/np.log2(N)
print("Robustness (Node importance) : ",R1)

# R2 = evaluator.VN_Entropy(A)/np.log(N)
# print("Robustness (VN entropy) : ",R2)

Aint = A.astype(int)

R3 = evaluator.Degree_Entropy(Aint)/np.log2(N)
print("Robustness (Degree distribution entropy) : ",R3)

# Degree counting
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())

fig, ax = plt.subplots()
plt.bar(deg, cnt, width=0.80, color='b')

plt.title("Degree Histogram")
plt.ylabel("Count")
plt.xlabel("Degree")
ax.set_xticks([d + 0.4 for d in deg])
ax.set_xticklabels(deg)
plt.show()

## Plotting the graph
nx.draw(G)
plt.show()
