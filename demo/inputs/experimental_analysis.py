import itertools
import numpy as np
import random
import timeit
import matplotlib.pyplot as plt
from networkx.algorithms import isomorphism
import bisect
import networkx as nx

##-------------------ALGORITHM 1: BRUTE-FORCE

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
    starttime = timeit.default_timer()
    degree_sequence_1 = get_degree_sequence(adj_1)
    degree_sequence_2 = get_degree_sequence(adj_2)
    if get_graph_order(adj_1) != get_graph_order(adj_2):
        res=False
        time = timeit.default_timer() - starttime
        return(time)
    elif np.array_equal(degree_sequence_1, degree_sequence_2) == False:
        res=False
        time = timeit.default_timer() - starttime
        return(time)
    else:
        for adj_matrix in list(
                map(lambda matrix: matrix["adj_matrix"],
                    get_all_vertex_permutations(adj_2))):
            if np.array_equal(adj_1, adj_matrix) == True:
                res=True
                time = timeit.default_timer() - starttime
                return(time)
    res=False
    time = timeit.default_timer() - starttime
    return(time)

##-------------------ALGORITHM 2: VF2
def algo2(adj_1,adj_2):
    G, G1 = nx.from_numpy_matrix(adj_1), nx.from_numpy_matrix(adj_2)
    starttime = timeit.default_timer()
    gm = nx.isomorphism.GraphMatcher(G, G1)
    gm.is_isomorphic()
    time = timeit.default_timer() - starttime
    return(time)

##-------------------ALGORITHM 3: WL
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

def wl_method(graph1, graph2):
        starttime = timeit.default_timer()
        graph_1_neighbour_list = neighbour_list(graph1)
        graph_2_neighbour_list = neighbour_list(graph2)

        n=len(graph1)

        # vertices' colors
        graph_1_colors = [0] * n
        graph_2_colors = [0] * n

        # repeat method method_dim times
        for i in range(1):
            # calc collections of neighbours' colors for each vertex
            graph_1_collection = []
            graph_2_collection = []
            for vertex in range(n):
                neighbours_colors = []
                for neighbour in graph_1_neighbour_list[vertex]:
                    bisect.insort(neighbours_colors, graph_1_colors[neighbour])
                graph_1_collection.append(neighbours_colors)
                neighbours_colors = []
                for neighbour in graph_2_neighbour_list[vertex]:
                    if(neighbour<len(graph_2_colors)):
                        bisect.insort(neighbours_colors, graph_2_colors[neighbour])
                graph_2_collection.append(neighbours_colors)

            # prepare color - collection pairs
            pairs = []
            color_index = 0
            for vertex in range(n):
                collection = graph_1_collection[vertex]
                if not collection in [row[1] for row in pairs]:
                    pairs.append([color_index, collection])
                    color_index += 1

            # check if all collections from graph_2 are in prepared pairs
            for vertex in range(n):
                if not graph_2_collection[vertex] in [row[1] for row in pairs]:
                    res=False
                    time = timeit.default_timer() - starttime
                    return(time)
                

            # assign new colors
            for vertex in range(n):
                graph_1_colors[vertex] = pairs[[row[1] for row in pairs].index(graph_1_collection[vertex])][0]
                graph_2_colors[vertex] = pairs[[row[1] for row in pairs].index(graph_2_collection[vertex])][0]

        # on the end compare vertices' colors
        for vertex in range(n):
            if graph_1_colors[vertex] != graph_1_colors[vertex]:
                res=False
                time = timeit.default_timer() - starttime
                return(time)

        # not returned False before
        res=True
        time = timeit.default_timer() - starttime
        return(time)
 


##------------------EXPERIMENT
testData=[]
n=[]
for i in range(2,21):
    t1='input' +str(i)+'_1a.txt'
    t2='input'+str(i)+'_2b.txt'
    testData.append(t1)
    testData.append(t2)
    n.append(i)

t1='input25_1a.txt'
t2='input25_2b.txt'
testData.append(t1)
testData.append(t2)
n.append(25)

t1='input30_1a.txt'
t2='input30_2b.txt'
testData.append(t1)
testData.append(t2)
n.append(30)

t1='input40_1a.txt'
t2='input40_2b.txt'
testData.append(t1)
testData.append(t2)
n.append(40)

#print(len(testData))

#print(testData)
#print(testData)

bt=[]
wt=[]
vt=[]
nb=[]

for j in range(2,15):
    adj_1 = np.loadtxt(testData[j], dtype=int)
    adj_2 = np.loadtxt(testData[j+1], dtype=int)
    tb=0
    tv=0
    tw=0
    for k in range(5):
     #   ansB=brute_force_test_graph_isomporphism(adj_1, adj_2)
        tb=tb+brute_force_test_graph_isomporphism(adj_1, adj_2)
        tv=tv+algo2(adj_1, adj_2)
        tw=tw+wl_method(adj_1, adj_2)
        
    bt.append(tb/5)
    wt.append(tw/5)
    vt.append(tv/5)
    nb.append(j)


#plot Results
plt.plot(nb,bt,label="Brute-Force")
plt.plot(nb,vt,label="VF2",color="orange")
plt.plot(nb,wt,label="Weisfeiler-Lehman",color="green")
plt.ylim(0, 0.001)
plt.legend()
#ax = plt.axes()
#ax.set_facecolor("black")
plt.xlabel("Number of Vertices")
plt.ylabel("Average Runtime")
#ax.set_ybound(lower=0, upper=1)
  
# Setting the background color of the plot 
# using set_facecolor() method
#ax.set_facecolor("black")
plt.show()


