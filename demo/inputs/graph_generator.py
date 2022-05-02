import numpy as np


def graph_generator(n,i):
    adjacency_matrix = np.random.randint(0,2,(n,n))
    if i==1:
        t='a'
    else:
        t='b'
    fp='input'+str(n)+'_'+str(i)+t+'.txt'
    print(fp)
    np.savetxt(fp,adjacency_matrix,fmt='%.2f')


###for i in range(18,20):
graph_generator(16,1)
graph_generator(16,2)
##graph_generator(11,1)
##graph_generator(11,2)
