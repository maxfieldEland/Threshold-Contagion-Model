# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 19:01:13 2018

@author: mgreen13
"""

import csv
import networkx as nx

#Create a empty Graph
g = nx.Graph()
#store all nodes
nodes = []
#store all possible edges 
edges = []

#read the random network's CSV file 
my_file = open("random_network.csv")
reader = csv.reader(my_file)
for row in reader:
    edges.append(row)
    if (int(row[0]) not in nodes):
        nodes.append(int(row[0]))
    if (int(row[1]) not in nodes):
        nodes.append(int(row[1]))
for i in nodes:
    g.add_node(i)

for j in edges:
    g.add_edge(int(j[0]),int(j[1]))

print ("Number of nodes: ", g.number_of_nodes())
print ("Number of edges: ", g.number_of_edges())

#Three lists that you want
degree = []
closeness = []
betweenness = []

for n in nodes:
    degree.append(nx.degree_centrality(g)[n])
    closeness.append(nx.closeness_centrality(g,None,None,True)[n])
    betweenness.append(nx.betweenness_centrality(g,None,True,None,False,None)[n])
print()
print("degree centrality: ")
print(degree,"\n")
print("closeness centrality: ")
print(closeness,"\n")
print("betweenness centrality: ")
print(betweenness,"\n")

# uncomment to test
#print(g.nodes())
#print(g.edges())

#print (nx.degree_centrality(g))
#print (nx.closeness_centrality(g,None,None,True))
#print (nx.betweenness_centrality(g,None,True,None,False,None))



import matplotlib.pyplot as plt
plt.hist(betweenness)