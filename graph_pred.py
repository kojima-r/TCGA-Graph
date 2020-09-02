import networkx as nx
import numpy as np
import scipy.stats as stats

# Erdős-Rényi graph
#G = nx.fast_gnp_random_graph(n=100,p=0.5)
# Barabási–Albert model
CG = nx.barabasi_albert_graph(n=cluster_num,m=10)
# Watts–Strogatz model
#G = nx.watts_strogatz_graph(n=100,k=3,p=0.1)

n=len(CG.nodes())
adj=[]
for i1,i2 in CG.edges():
  adj.append([i1,i2])
print(len(adj))
print(n)


