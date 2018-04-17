# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 08:41:18 2018

@author: mgreen13
"""

import numpy as np
#import plotly.plotly as py
#from plotly.graph_objs import*
import random
import matplotlib.pyplot as plt
import math
import networkx as nx
import re
import csv

#from drawingNet import draw_graph


#****************************************************** Supporting Methods************************************************

# Load Data into numpy array, toss first row and first column
def load_data(filename):
    c = np.loadtxt(open(filename,'rb'),delimiter = ",")
   # Delete the first column of matrix to get adj matrix
    return c  

def edge_to_adj(c):
    max1 = max(map(lambda x: x[0], c))+1
    max2 = max(map(lambda x: x[1], c)) + 1
    nodes = max([max1,max2])
    
    adjList = [[] for k in range(nodes)]
    edge_u = []
    edge_v = []
    for k,i in enumerate(c):
        edge_u.append(c[k][0])
        edge_v.append(c[k][1])
        
    for k,i in enumerate(edge_u):
        u = int(edge_u[k]-1)
        v = int(edge_v[k]-1)
        adjList[u].append(int(v))
        adjList[v].append(int(u))

    return adjList

""" G(N,M): M edges distributed at random among N nodes Considering the relationship between N and M """
def G(N,M):    
    # N = number of node in network
    # M = number of edges in network
    mat = np.zeros(shape = (int(M),2))
    
    # randomly select M edges from list
    j = 0
    # create M edges between nodes 
    while j < M:
        r = random.randint(0,N-1)
        c = random.randint(0,N-1)
        mat[j,0] = r
        mat[j,1] = c
        j=j+1  
    return mat.astype(int) 



class Node(object):
    
    def __init__(self,state,neighbours):
        # all nodes start off
        self.state = state
        
        # threshold function boundarys
        self.thetaOn = None
        self.thetaOff = None
        
        # list of nodes neighbours
        self.neighbours = neighbours 
        self.future_state = None
        
        # set threshold of node
        self.set_threshhold()
        
        # keep track of nodes on/off period 
        self.period  = [0]
        
        self.periodicity = None
    
    # set the future state of the nodes
    def set_future_state(self,future_state):
       self.future_state = future_state
      
    def set_state(self, state):
        self.state = state
      
    def set_seed(self, state):
        self.state =1
        
    def get_future_state(nodes,n):
       return(nodes[n].future_state)
    
    def get_state(nodes, n):
        return(nodes[n].state)
        
    def set_threshhold(self):
        self.thetaOff = random.uniform(1/2,1)
        self.thetaOn = random.uniform(0,1/2)
        
    def get_threshhold(self):
        return [self.thetaOn,self.thetaOff]
    # state change threshold based on state of neighbours in synch
    
    # nodes: list of node objects
    def update(nodes):
       for node in nodes:
           # list of neigbours states
           states = []
           # looping over indexs of neighbours in nodes vector
           for n in node.neighbours:
               # get state of each neighbour
               states.append(Node.get_state(nodes,n))
            # set future state of node to one if average of neighbour states is within threshold of node
           if(node.thetaOn <= np.average(states) < node.thetaOff) :
               Node.set_future_state(node,1)
               node.period.append(1)
           else: 
               Node.set_future_state(node, 0)
               node.period.append(0)
        # set current state to future state
       for k,node in enumerate(nodes):
           temp_future_state = Node.get_future_state(nodes,k)
           Node.set_state(node,temp_future_state)
           
           
    def reset(nodes):
        for node in nodes:
            node.state = 0
    


# for each possible period, scan string and remember longest periodic subsequence
# return the number of repetitions of the largest substring, the length of the period and 
#the position in cycle began in the string

def find_period(src):
  best = (0, 0, 0) # repetitions-1, period, position
  period = 0
  while period < len(src) // max(2, 1 + best[IREP]): # floor division will round down to nearest whole number
    period += 1
    length = 0
    for pos in range(len(src) - 1 - period, -1, -1):
      if src[pos] == src[pos + period]:
        length += 1
        repetitions = length // period
        if repetitions >= best[IREP]:
          best = (repetitions, period, pos)
      else:
        length = 0
  return best







#********************************************************** main methods ***********************************************


# generate random network with poisson distributed 
c = G(1000, (17/2)*1000)

# write edge list to CSV
with open('random_network.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(c)
    

d = edge_to_adj(c)


    
nodes = []

for index, node in enumerate(d):
    # initialize state of node and give list of nodes nieghbours
    nodes.append(Node(0,d[index]))


#********************************************************** Macro Period Analysis ***************************************
# O(N^3) or worse :(
# generate 100 macro periods from fixed determestic random network
macro_periods = []
collapse_time = []
seed_nodes = []
for i in list(range(100)):
    # RESET NODE STATE
    Node.reset(nodes)
    # SET NODE SEED RANDOMLY
    node_select = random.randint(0,(len(d)-1))
    Node.set_seed(nodes[node_select],1)
    # TRACK WHICH NODES ARE BEING SELECTED AS THE SEED
    seed_nodes.append(node_select)
    active = []
    node_selected = []
    # UPDATE NETWORK N TIMES
    for i in list(range(1000)):
        # keep track of states of each node in network after 
        states = []
        for node in nodes:
            states.append(node.state) 
        Node.update(nodes)
        active.append(np.average(states))
  
    #period detection
    IREP, IPER, IPOS = 0, 1, 2
    s = active
    res = find_period(s)
    macro_periods.append(res[1])
    collapse_time.append(res[2])

x = list(range(1000))


plt.scatter(x,active)
plt.title("Active Fraction of Nodes over Time")
plt.xlabel("Iterates")
plt.ylabel("Active Fraction")


plt.hist(macro_periods)
plt.hist(collapse_time)

data = []
