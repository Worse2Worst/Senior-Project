from matplotlib import patches as patches, pyplot as plt
import matplotlib.cm as cm
from matplotlib import colors
from itertools import cycle
import numpy as np

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


def draw_original_nodes(nodes):
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
    plt.show()

def draw_requests(requests):
    c=[] # array 'c' to remeber the colors

    # Separate requests by color
    colormap = plt.cm.gist_ncar  # nipy_spectral, Set1,Paired
    colorst = [colormap(i) for i in np.linspace(0, 0.9, len(requests))]
    for t, j1 in enumerate(requests):
        c.append(colorst[t])

    # drawing the requests
    for i in range(len(requests)):
        p = requests[i][0]
        d = requests[i][1]
        plt.scatter(p.x, p.y,color=c[i])
        plt.scatter(d.x, d.y,color=c[i])
    plt.show()
    '''
    ####### For Saving Pictures into files ###########################
    base = os.path.splitext(os.path.basename(filename))[0]+'.png'
    dir = 'pics/original/'
    save_path = dir+base
    plt.savefig(save_path)
    '''