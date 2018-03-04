from matplotlib import patches as patches, pyplot as plt
from pylab import *
from matplotlib import collections  as mc
import pylab as pl
import matplotlib.cm as cm
from matplotlib import colors
from itertools import cycle
import numpy as np
import mplcursors
# Unfinished!!!!!

def draw_original_nodes(LOCATIONS, REQUESTS):
    # Description text
    fig, ax = plt.subplots()
    ax.set_title("The original nodes")
    nodes=[]
    #gca().set_position((.1, .3, .8, .6))  # to make a bit of room for extra text
    depot = 0  # get the depot!!!
    ##### Legends ###############################
    red_patch = patches.Patch(color='red', label='Pickup nodes')
    blue_patch = patches.Patch(color='blue', label='Delivery nodes')
    #plt.legend(handles=[blue_patch])
    plt.legend([red_patch, blue_patch], ['Pickup nodes', 'Delivery nodes'])

    for req in REQUESTS.values():
        p,d = req[0],req[1]
        pX,pY = LOCATIONS[p][0], LOCATIONS[p][1]
        dX,dY = LOCATIONS[d][0], LOCATIONS[d][1]
        plt.scatter(pX, pY, c='red')
        plt.scatter(dX, dY, c='blue')
    plt.scatter(LOCATIONS[depot][0], LOCATIONS[depot][1], c='silver')  # draw the depot
    figtext(.02, .02, 'Have ' + str(len(LOCATIONS) - 1) + ' nodes (not counting the depot)')
    mplcursors.cursor(hover=True)
    plt.show()


def draw_nodes_with_added_depots(LOCATIONS, REQUESTS,DEPOTS):
    # Description text
    fig, ax = plt.subplots()
    ax.set_title("The original nodes")
    nodes=[]
    #gca().set_position((.1, .3, .8, .6))  # to make a bit of room for extra text
    ##### Legends ###############################
    red_patch = patches.Patch(color='red', label='Pickup nodes')
    blue_patch = patches.Patch(color='blue', label='Delivery nodes')
    #plt.legend(handles=[blue_patch])
    plt.legend([red_patch, blue_patch], ['Pickup nodes', 'Delivery nodes'])

    for req in REQUESTS.values():
        p,d = req[0],req[1]
        pX,pY = LOCATIONS[p][0], LOCATIONS[p][1]
        dX,dY = LOCATIONS[d][0], LOCATIONS[d][1]
        plt.scatter(pX, pY, c='red')
        plt.scatter(dX, dY, c='blue')
    for i,dep in enumerate(DEPOTS.values()):
        plt.scatter(DEPOTS[i][0], DEPOTS[i][1], c='silver')  # draw the depot
    figtext(.02, .02, 'Have ' + str(len(LOCATIONS) - 1) + ' nodes (not counting the depot)')
    mplcursors.cursor(hover=True)
    plt.show()



def draw_requests(LOCATIONS,REQUESTS):
    c=[] # array 'c' to remeber the colors
    fig, ax = plt.subplots()
    ax.set_title("The Requests, separated by colors")
    # Separate requests by color
    colormap = plt.cm.gist_ncar  # nipy_spectral, Set1,Paired
    colorst = [colormap(i) for i in np.linspace(0, 0.9, len(REQUESTS))]
    for t, j1 in enumerate(REQUESTS):
        c.append(colorst[t])

    # drawing the requests
    for i in range(len(REQUESTS)):
        p = REQUESTS[i][0]
        d = REQUESTS[i][1]
        sc = plt.scatter(LOCATIONS[p][0], LOCATIONS[p][1],color=c[i])
        sc = plt.scatter(LOCATIONS[d][0], LOCATIONS[d][1],color=c[i])
    figtext(.02, .02, 'Have ' + str(len(REQUESTS)) + ' requests')
    plt.show()

    '''
    ####### For Saving Pictures into files ###########################
    base = os.path.splitext(os.path.basename(filename))[0]+'.png'
    dir = 'pics/original/'
    save_path = dir+base
    plt.savefig(save_path)
    '''


def draw_tours(chromosome, LOCATIONS, depot=0):
    line_array = []
    x_depot, y_depot = LOCATIONS[depot][0], LOCATIONS[depot][1]
    dep = [x_depot, y_depot]
    numberOfTours = 0
    for [num_car,req,tour] in chromosome:
        if (len(tour) > 0):
            lines = []
            x_first, y_first = LOCATIONS[tour[0]][0], LOCATIONS[tour[0]][1]  # first node in tour
            x_last, y_last = LOCATIONS[tour[-1]][0], LOCATIONS[tour[-1]][1] # last node in tour
            first_point = [x_first,y_first]
            last_point = [x_last,y_last]
            lines.append((dep,first_point)) # Draw a line that connects first point to depot
            for i in range(len(tour) - 1):
                from_index, to_index = int(tour[i]), int(tour[i + 1])
                x_from, y_from = LOCATIONS[from_index][0], LOCATIONS[from_index][1]
                a = [x_from, y_from]
                x_to, y_to = LOCATIONS[to_index][0], LOCATIONS[to_index][1]
                b = [x_to, y_to]
                point = (a, b)
                lines.append(point)
            lines.append((dep,last_point)) # Draw a line that connects last point to depot
            numberOfTours += 1
            line_array.append(lines)
    # flat out list
    #flat_list = [item for sublist in line_array for item in sublist]


    fig, ax = pl.subplots()
    ax.set_title("The Routes(Tours), separated by colors")
    # gca().set_position((.1, .3, .8, .6))  # to make a bit of room for extra text
    c = []  # array 'c' to remeber the colors
    # Separate clusters by color
    colormap = plt.cm.gist_ncar  # nipy_spectral, Set1,Paired
    colorst = [colormap(i) for i in np.linspace(0, 0.9, len(line_array))]
    for t, j1 in enumerate(line_array):
        c.append(colorst[t])
    i = 0
    for lines in line_array:
        lc = mc.LineCollection(lines,colors=c[i], linewidths=2)
        ax.add_collection(lc)
        ax.autoscale()
        ax.margins(0.1)
        i += 1
        #plt.scatter(depot.x, depot.y, s=30)
    figtext(.02, .02,
            'Have ' + str(numberOfTours) + ' tours. ')
    plt.show()

