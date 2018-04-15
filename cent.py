import networkx as nx

#Create a empty Graph
g = nx.Graph()

# add 4 nodes into it and set a defalut state, which is 0
g.add_nodes_from([1,33,55,65], state = 0)
# link 1, 33, 65
g.add_edges_from([(1,33),(33,65)])

print (g.number_of_nodes())
print (g.number_of_edges())

print(g.nodes())
print(g.edges())

print("Graph with state: ", g.nodes(True))

print("**********")
# Centrality of Nodes
print (nx.degree_centrality(g))
print (nx.closeness_centrality(g,None,None,True))
print (nx.betweenness_centrality(g,None,True,None,False,None))
