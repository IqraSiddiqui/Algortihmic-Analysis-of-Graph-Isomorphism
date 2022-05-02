##Credits: https://github.com/sewerus/grismo/blob/5c19f30546c38b1714e50dd0cc49b97584820cc0/isomorfism_test.py#L27

#---------------

import itertools
import numpy as np
import random
import timeit
import matplotlib.pyplot as plt
import bisect

from regex import T

def neighbour_list(matrix):
    result = []
    n = len(matrix)
    for i in range(n):
        result.append([])
    for i in range(n - 1):
        for j in range(i, n):
            if matrix[i][j]:
                result[i].append(j)
                result[j].append(i)
    return result

def wl_method(G1, G2, k_dim ):
        G1_neighbors = neighbour_list(G1)
        G2_neighbors = neighbour_list(G2)

        if (len(G1) != len(G2)):
            return False
        
        n = len(G1)

        # Initial coloring or vertices
        G1_colors = [0] * n
        G2_colors = [0] * n

        # repeat method k_dim times
        for i in range(k_dim):
            # store collections of neighbours' colors for each vertex
            G1_collections = []
            G2_collections = []
            for vertex in range(n):
                neighbours_colors = []
                for neighbour in G1_neighbors[vertex]:
                    bisect.insort(neighbours_colors, G1_colors[neighbour])
                G1_collections.append(neighbours_colors)
                neighbours_colors = []
                for neighbour in G2_neighbors[vertex]:
                    bisect.insort(neighbours_colors, G2_colors[neighbour])
                G2_collections.append(neighbours_colors)

            # prepare color - collection pairs
            pairs = []
            color_index = 0
            for vertex in range(n):
                collection = G1_collections[vertex]
                if not collection in [row[1] for row in pairs]:
                    pairs.append([color_index, collection])
                    color_index += 1

            # check if all collections from graph_2 are in prepared pairs
            for vertex in range(n):
                if not G2_collections[vertex] in [row[1] for row in pairs]:
                    return False

            # assign new colors
            for vertex in range(n):
                G1_colors[vertex] = pairs[[row[1] for row in pairs].index(G1_collections[vertex])][0]
                G2_colors[vertex] = pairs[[row[1] for row in pairs].index(G2_collections[vertex])][0]

        # Check whether both graphs have same coloring in the end
        for vertex in range(n):
            if G1_colors[vertex] != G1_colors[vertex]:
                return False

        # return True as graphs are isomorphic
        return True
 

#----------------------------TESTING
testData1=[]
testData2=[]
for i in range(2,21):
    t1='inputs\input' +str(i)+'_1a.txt'
    t2='inputs\input'+str(i)+'_2b.txt'
    testData1.append(t1)
    testData2.append(t2)
bw=[]
nw=[]
for i in range (2,15):
    adj_1 = np.loadtxt(testData1[i], dtype=int)
    adj_2 = np.loadtxt(testData2[i], dtype=int)
    print("n = ", i, wl_method(adj_1,adj_2, 3))

for j in range(2,15):
   adj_1 = np.loadtxt(testData1[1], dtype=int)
   adj_2 = np.loadtxt(testData2[1], dtype=int)
   t=0
   for k in range(5):
       ansB = wl_method(adj_1, adj_2, 3)
       t = t+timeit.timeit("wl_method", setup="from __main__ import wl_method")
   bw.append(t/5)
   nw.append(j)
print(bw)
print(nw)
#plot Results
# plt.style.use('dark_background')
plt.plot(nw, bw, label="WL", color = 'g')
plt.legend()
plt.xlabel("Number of Vertices")
plt.ylabel("Average Runtime")
plt.show()

