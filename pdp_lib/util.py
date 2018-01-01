from matplotlib import patches as patches, pyplot as plt
from pylab import *
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
    res += 'req_type = ' + str(v.req_type)
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

