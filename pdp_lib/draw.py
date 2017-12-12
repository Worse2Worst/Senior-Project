import os
import numpy as np
import matplotlib.pyplot as plt
from collections import namedtuple
from datetime import datetime, timedelta
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.lines as mlines
from matplotlib import collections  as mc
import pylab as pl

def draw_nodes(nodes):
    locations=[]
    req_types=[]
    nodes.pop(0)  # remove the depot!!!
    ##### Legends ###############################
    red_patch = patches.Patch(color='red', label='Pickup nodes')
    blue_patch = patches.Patch(color='blue', label='Delivery nodes')
    #plt.legend(handles=[blue_patch])
    plt.legend([red_patch, blue_patch], ['Pickup nodes', 'Delivery nodes'])

    for p in nodes:
        locations.append([p.x,p.y])
        req_types.append(p.req_type)
    for i in range(len(locations)):
        x = locations[i][0]
        y = locations[i][1]
        color = 'red' if (req_types[i] == 'p') else 'blue'
        plt.scatter(x, y,c=color)

    plt.show()