# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import sys


def distance(ax,ay, bx , by):
        xDist = abs(ax-bx)
        yDist = abs(ay-by)
        distance = np.sqrt((xDist**2)+(yDist**2))
        return distance

if __name__ == "__main__":
    filename = sys.argv[1]
    file = open('Data/'+filename,'r')

    arr = []
    edge_list = []
    for line in file:
        arr.append(line.split())

    #remove text
    arr = arr[6:]
    del arr[-1]


    #build graph
    G = nx.Graph()
    for i in range (len(arr)):
        for j in range(len(arr)):
            if arr[i][0] != arr[j][0]:
                ax = float(arr[i][1])
                ay = float(arr[i][2])
                bx = float(arr[j][1])
                by = float(arr[j][2])

                d = distance(ax,ay,bx,by)

                edge_list.append((arr[i][0],arr[j][0],d))


    G.add_weighted_edges_from(edge_list)
    g_edges = G.edges(data=True)

    # Make MST
    T=nx.minimum_spanning_tree(G)



    tree_edges = T.edges(data=True)


    T2 = nx.MultiDiGraph(T)
    tree_edges = T2.edges(data=True)

    #Eulerian Path
    C = list(nx.eulerian_circuit(T2,"1"))

    C2 =[]

    for i in range(len(C)):
        C2.append(C[i][0])
    C2.append(C2[0])

    pruned_list = []
    for i in range(len(C2)):
        if C2[i] not in pruned_list:
            pruned_list.append(C2[i])

    pruned_list.append(C2[0])

    num=0
    for i in range (1,len(pruned_list)):

        ax=[item[1] for item in arr if item[0]==pruned_list[i-1]][0]
        ay=[item[2] for item in arr if item[0]==pruned_list[i-1]][0]
        bx=[item[1] for item in arr if item[0]==pruned_list[i]][0]
        by=[item[2] for item in arr if item[0]==pruned_list[i]][0]

        d = distance(float(ax),float(ay),float(bx),float(by))
        #print(d)
        num+=d

    print("Best route:",pruned_list)
    print("Best Distance:",num)
