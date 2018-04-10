# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 15:51:24 2018
Input d:adjacency list,and c: edge list
@author: mgreen13
"""

import random 
import matplotlib.pyplot as plt

def draw_graph(c,d):
    """`graph` is a nx.Graph. `posX` and `posY` are dicts mapping node
    to x- or y-coordinate.
    
    Returns nothing, but plots the graph.
    
    TODO: Color node based on state of node
    """
    plt.figure(figsize=(10,10))

    posX = {}
    posY = {}
    for n,i in enumerate(c):
        posX[n] = random.random()
        posY[n] = random.random()
    
    # first plot edges as black lines:
    for i,j in c:
        xi = posX[i]
        xj = posX[j]
        yi = posY[i]
        yj = posY[j]
        
        plt.plot( [xi,xj], [yi,yj], 'k-', lw=1.5)
    
    # now plot nodes:
    nodeList = list(range(len(d)))
    Xs = [ posX[n] for n in nodeList ]
    Ys = [ posY[n] for n in nodeList ]
    
    # color nodes according to state
   
    plt.plot(Xs,Ys, 'o', ms=10, c="#ff9966", clip_on=False)
    
    plt.axis("off")
    plt.show()
    
