##-------------------ALGORITHM 2: VF2
import timeit
import matplotlib.pyplot as plt
from networkx.algorithms import isomorphism
import bisect
import networkx as nx

import numpy as np

def algo2(adj_1,adj_2):
    G1=nx.from_numpy_matrix(adj_1)
    G2=nx.from_numpy_matrix(adj_2)
    GM = isomorphism.GraphMatcher(G1,G2)
    return(GM.is_isomorphic())

#--Testing

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


#-plotting
vt=[]
nb=[]
for j in range(2,43):
    adj_1 = np.loadtxt(testData[j], dtype=int)
    adj_2 = np.loadtxt(testData[j+1], dtype=int)
    #tb=0
    tv=0
    tw=0
    for k in range(5):
     #   ansB=brute_force_test_graph_isomporphism(adj_1, adj_2)
      #  tb=tb+timeit.timeit("brute_force_test_gr aph_isomporphism", setup="from __main__ import brute_force_test_graph_isomporphism")
        ansV=algo2(adj_1, adj_2)
        print(ansV)
        tv=tv+timeit.timeit("algo2", setup="from __main__ import algo2")
        #ansW=wl_method(adj_1, adj_2)
        #tw=tw+timeit.timeit("wl_method", setup="from __main__ import wl_method")             
    #bt.append(tb/5)
    #wt.append(tw/5)
    vt.append(tv/5)
    nb.append(j)


#plot Results
#plt.plot(nb,bt,label="Brute-Force")
plt.plot(nb,vt,label="VF2",color="orange")
#plt.plot(nb,wt,label="Weisfeiler-Lehman",color="green")
plt.legend()
plt.xlabel("Number of Vertices")
plt.ylabel("Average Runtime")
plt.show()
