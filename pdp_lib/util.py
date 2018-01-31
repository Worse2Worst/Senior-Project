from matplotlib import patches as patches, pyplot as plt
from pylab import *
from matplotlib import collections  as mc
import pylab as pl
import matplotlib.cm as cm
from matplotlib import colors
from itertools import cycle
import numpy as np
import mplcursors


def print_node(v):
    res = ''
    res += 'index = ' + str(v.index) + ' ,'
    res += 'x = ' + str(v.x) + ' ,'
    res += 'y = ' + str(v.y) + ' ,'
    res += 'ET = ' + str(v.ET) + ' ,'
    res += 'LT = ' + str(v.LT) + ' ,'
    res += 'p_sibling = ' + str(v.p_sib) + ' ,'
    res += 'd_sibling = ' + str(v.d_sib) + ' ,'
    res += 'req_type = ' + str(v.req_type)+' ,'
    res += 'depot_num =' + str(v.depot)
    print(res)

def print_distances(dis):
    n = len(dis)
    for i in range(n):
        temp = ''
        for j in range(n):
            temp+= str(dis[i][j]) + ' '
        print (temp)

def print_nodes(nodes):
    for v in nodes:
        print_node(v)

def print_requests(requests):
    for r in requests:
        res=''
        res += 'p_node = ' + str(r[0].index)+' ,'
        res += 'at(' + str(r[0].x)+','+ str(r[0].y) + '),'
        res += 'ET = ' + str(r[0].ET) + ' ,'
        res += 'LT = ' + str(r[0].LT) + ' ,'+'\t\t\t'
        res += 'd_node = ' + str(r[1].index) + ' ,'
        res += 'at(' + str(r[1].x)+',' + str(r[1].y) + ')'+','
        res += 'ET = ' + str(r[1].ET) + ' ,'
        res += 'LT = ' + str(r[1].LT) + ' ,' + '\t\t\t'
        print (res)

def print_clusters(clusters):
    n = len(clusters)
    print ('Have '+ str(n)+' clusters')
    for i in range(n):
        print ('#cluster #'+str(i+1)+'-----------')
        print_requests(clusters[i])
        print ('--------------------------')

def draw_added_nodes(nodes):
    # Description text
    fig, ax = plt.subplots()
    ax.set_title("The nodes, added depots")
    #gca().set_position((.1, .3, .8, .6))  # to make a bit of room for extra text
    locations = []
    req_types = []
    depots = nodes[-5:]  # get the depots!!!
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

    # draw the depots
    for d in depots:
        plt.scatter(d.x, d.y, c='silver')

    figtext(.02, .02, 'Have ' + str(len(nodes)-6) + ' nodes (not counting the depots)')
    mplcursors.cursor(hover=True)
    plt.show()

def draw_original_nodes(nodes):
    # Description text
    fig, ax = plt.subplots()
    ax.set_title("The original nodes")
    #gca().set_position((.1, .3, .8, .6))  # to make a bit of room for extra text
    locations = []
    req_types = []
    depot = nodes[0]  # get the depot!!!
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


    plt.scatter(depot.x, depot.y, c='silver')  # draw the depot, just in case
    figtext(.02, .02, 'Have ' + str(len(nodes)-1) + ' nodes (not counting the depot)')
    mplcursors.cursor(hover=True)
    plt.show()


def draw_requests(requests):
    c=[] # array 'c' to remeber the colors
    fig, ax = plt.subplots()
    ax.set_title("The Requests, separated by colors")
    # Separate requests by color
    colormap = plt.cm.gist_ncar  # nipy_spectral, Set1,Paired
    colorst = [colormap(i) for i in np.linspace(0, 0.9, len(requests))]
    for t, j1 in enumerate(requests):
        c.append(colorst[t])

    # drawing the requests
    for i in range(len(requests)):
        p = requests[i][0]
        d = requests[i][1]
        sc = plt.scatter(p.x, p.y,color=c[i])
        sc = plt.scatter(d.x, d.y,color=c[i])
    figtext(.02, .02, 'Have ' + str(len(requests)) + ' requests')

    plt.show()

    '''
    ####### For Saving Pictures into files ###########################
    base = os.path.splitext(os.path.basename(filename))[0]+'.png'
    dir = 'pics/original/'
    save_path = dir+base
    plt.savefig(save_path)
    '''

def draw_clusters(clusters):
    fig, ax = plt.subplots()
    ax.set_title("The clusters, separated by colors")
    #gca().set_position((.1, .3, .8, .6))  # to make a bit of room for extra text
    c=[] # array 'c' to remeber the colors
    # Separate clusters by color
    colormap = plt.cm.gist_ncar  # nipy_spectral, Set1,Paired
    colorst = [colormap(i) for i in np.linspace(0, 0.9, len(clusters))]
    for t, j1 in enumerate(clusters):
        c.append(colorst[t])

    # drawing the clusters
    i=0
    for cluster in clusters:
        for j in range(len(cluster)):
            p = cluster[j][0]
            d = cluster[j][1]
            plt.scatter(p.x, p.y,color=c[i])
            plt.scatter(d.x, d.y,color=c[i])
        i+=1
    figtext(.02, .02, 'Have ' + str(len(clusters)) + ' clusters')
    plt.show()

def draw_cluster(cluster):
    draw_requests(cluster)

def draw_nodes_depots(nodes,depots):
    # Description text
    fig, ax = plt.subplots()
    ax.set_title("The nodes, separated by depots")
    locations = []
    depot_num = []
    dep = [0] * len(depots)
    ##### Legends ###############################
    red_patch = patches.Patch(color='red', label='Depot 0')
    blue_patch = patches.Patch(color='blue', label='Depot 1')
    green_patch = patches.Patch(color='green', label='Depot 2')
    yellow_patch = patches.Patch(color='yellow', label='Depot 3')
    purple_patch = patches.Patch(color='purple', label='Depot 4')
    # plt.legend(handles=[blue_patch])
    plt.legend([red_patch, blue_patch,green_patch,yellow_patch,purple_patch], ['Depot 0','Depot 1','Depot 2','Depot 3','Depot 4'])

    for v in nodes:
        locations.append([v.x, v.y])
        depot_num.append(v.depot)
        dep[int(v.depot)] +=1
    for i in range(len(locations)):
        x = locations[i][0]
        y = locations[i][1]
        color = 'black'
        if (depot_num[i] == 0): color = 'red'
        elif (depot_num[i] == 1): color = 'blue'
        elif (depot_num[i] == 2): color = 'green'
        elif (depot_num[i] == 3): color = 'yellow'
        elif (depot_num[i] == 4): color = 'purple'
        plt.scatter(x, y, c=color)

    # draw the depots
    for d in depots:
        plt.scatter(d.x, d.y, c='silver')
    dep_stat=''
    dep_stat += str(dep[0])+','+str(dep[1])+','+str(dep[2])+','+str(dep[3])+','+str(dep[4])
    figtext(.02,.02, 'Have ' + str(len(nodes) - 1) + ' nodes (not counting the depots), '+'Depot 0,1,2,3,4 have '+dep_stat)
    mplcursors.cursor(hover=True)
    plt.show()

def draw_tours(tours, nodes,depot):
    line_array = []
    for tour in tours:
        lines = []
        x_depot, y_depot = depot.x, depot.y
        x_first, y_first = nodes[tour[0]].x, nodes[tour[0]].y
        x_last, y_last = nodes[tour[-1]].x, nodes[tour[-1]].y
        dep = [x_depot,y_depot]
        first_point = [x_first,y_first]
        last_point = [x_last,y_last]

        lines.append((dep,first_point))
        for i in range(len(tour) - 1):
            from_index, to_index = int(tour[i]), int(tour[i + 1])
            x_from, y_from = nodes[from_index].x, nodes[from_index].y
            a = [x_from, y_from]
            x_to, y_to = nodes[to_index].x, nodes[to_index].y
            b = [x_to, y_to]
            point = (a, b)
            lines.append(point)

        lines.append((dep,last_point))
        line_array.append(lines)
    # flat out list
    flat_list = [item for sublist in line_array for item in sublist]

    lc = mc.LineCollection(flat_list, linewidths=2)
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
        #plt.scatter(depot.x, depot.y, s=30)
    plt.show()

'''
    #print job
    def print_sol(p_jobs):
        i = 0
        for tour in p_jobs:
            s = 'Vehicle ' + str(i) +' :'
            for node in tour:
                s+=str(node) + '->'
'''