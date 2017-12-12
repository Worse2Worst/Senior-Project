import os
from pdp_lib import preprocess
import matplotlib.pyplot as plt
from collections import namedtuple
from datetime import datetime, timedelta
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.lines as mlines
from matplotlib import collections  as mc
import pylab as pl


def save_original_nodes(nodes, filename):
    locations = []
    req_types = []
    depot = nodes.pop(0)  # remove the depot!!!
    plt.scatter(depot.x, depot.y, c='silver')  # draw the depot, just in case
    ##### Legends ###############################
    red_patch = patches.Patch(color='red', label='Pickup nodes')
    blue_patch = patches.Patch(color='blue', label='Delivery nodes')
    # plt.legend(handles=[blue_patch])
    plt.legend([red_patch, blue_patch], ['Pickup nodes', 'Delivery nodes'])

    for p in nodes:
        locations.append([p.x, p.y])
        req_types.append(p.req_type)
    for i in range(len(locations)):
        x = locations[i][0]
        y = locations[i][1]
        color = 'red' if (req_types[i] == 'p') else 'blue'
        plt.scatter(x, y, c=color)
    base = os.path.splitext(os.path.basename(filename))[0]+'.png'
    dir = 'pics/original/'
    save_path = dir+base
    plt.savefig(save_path)

def save_all_pics(dir_main= 'pdp_instances/LiLim/'):
    for dir_sub in os.listdir(dir_main):
        if not os.path.isfile(dir_main + dir_sub + '/'):
            directory = dir_main + dir_sub + '/'
            for fn in os.listdir(directory):
                fn = directory + fn
                nodes = preprocess.read_node(fn)
                save_original_nodes(nodes, fn)

