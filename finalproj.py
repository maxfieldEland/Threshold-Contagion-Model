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
import plotly.plotly as py
from plotly.graph_objs import*
import math
import networkx as nx
import re

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
    
  
# determine if there is a periodic orbit of less than 2^s
# input list of nodes, check for periodic state switch
def period_check(nodes):
    for node in nodes:
        for i in list(range(len(nodes))):
            # throw away burnout
            if i > len(nodes)/2:
                if node.period[i] == node.period[i+1]:
                    node.periodicity = 1
                
REPEATER = re.compile(r"(.+?)\+$")

def repeated(s):
    match = REPEATER.match(s)
    return match.group(1) if match else None


#********************************************************** main methods ***********************************************

# generate random network with poisson distributed 
c = G(1000, (17/2)*1000)
d = edge_to_adj(c)


nodes = []

for index, node in enumerate(d):
    # initialize state of node and give list of nodes nieghbours
    nodes.append(Node(0,d[index]))

# implement seed and time series
Node.set_seed(nodes[random.randint(0,len(d))],1)

# take n time steps

for i in list(range(1000)):
    states = []
    for node in nodes:
        states.append(node.state) 
    Node.update(nodes)
    
  

# TODO Implement 
for i in list(range(10)):
    
    sub = repeated(''.join(map(str,nodes[i].period)))
    if sub:
        print("%r: %r"%(i,sub))
    else:
        print("%r does not repeat." %i)



