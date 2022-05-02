##Credits: https://tonicanada.medium.com/brute-force-code-for-isomorphisms-1241ef180570

#input: two graphs in adjency matrix representation
#output: Boolean i.e. True if both graphs are isomorphic otherwise false
#---------------

import itertools
import numpy as np
import random
import timeit
import matplotlib.pyplot as plt


def get_graph_order(adj_matrix):
    if len(adj_matrix) != len(adj_matrix[0]):
        return -1
    else:
        return len(adj_matrix)


def get_degree_sequence(adj_matrix):
    degree_sequence = []
    for vertex in range(len(adj_matrix)):
        degree_sequence.append(sum(adj_matrix[vertex]))
    degree_sequence.sort(reverse=True)
    return degree_sequence


def get_all_vertex_permutations(adj_matrix):
    all_adj_matrix = []
    idx = list(range(len(adj_matrix)))
    possible_idx_combinations = [
        list(i) for i in itertools.permutations(idx, len(idx))
    ]
    for idx_comb in possible_idx_combinations:
        a = adj_matrix
        a = a[idx_comb]
        a = np.transpose(np.transpose(a)[idx_comb])
        all_adj_matrix.append({
            "perm_vertex":
            idx_comb,
            "adj_matrix":
            a
        })

    return all_adj_matrix


def brute_force_test_graph_isomporphism(adj_1, adj_2):
    degree_sequence_1 = get_degree_sequence(adj_1)
    degree_sequence_2 = get_degree_sequence(adj_2)
    if get_graph_order(adj_1) != get_graph_order(adj_2):
        return False
    elif np.array_equal(degree_sequence_1, degree_sequence_2) == False:
        return False
    else:
        for adj_matrix in list(
                map(lambda matrix: matrix["adj_matrix"],
                    get_all_vertex_permutations(adj_2))):
            if np.array_equal(adj_1, adj_matrix) == True:
                return True
    return False

#----------------------------TESTING
#print(brute_force_test_graph_isomporphism(adj_1, adj_2))

testData=[]
n=[]
for i in range(2,21):
    t1='input' +str(i)+'_1a.txt'
    t2='input'+str(i)+'_2b.txt'
    testData.append(t1)
    testData.append(t2)
    n.append(i)
#print(testData)
#print(testData)

bt=[]
nb=[]

for j in range(2,15):
    adj_1 = np.loadtxt(testData[j], dtype=int)
    adj_2 = np.loadtxt(testData[j+1], dtype=int)
    t=0
    for k in range(5):
        ansB=brute_force_test_graph_isomporphism(adj_1, adj_2)
        t=t+timeit.timeit("brute_force_test_graph_isomporphism", setup="from __main__ import brute_force_test_graph_isomporphism")
        
    bt.append(t/5)
    nb.append(j)
print(bt)
print(nb)
#print(n)
#plot Results
plt.plot(nb,bt,label="Brute-Force")
#plt.plot(ns,pt,label="Prims")
plt.legend()
plt.xlabel("Number of Vertices")
plt.ylabel("Average Runtime")
plt.show()



