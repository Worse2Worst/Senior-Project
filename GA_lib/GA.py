import os
import time
import numpy as np
import random
from random import randrange,randint
from pdp_lib import preprocessing
from pdp_lib import save_pics
from pdp_lib import util
from pdp_lib import processing


global filename
global nodes
global requests
global distances




# A couple is the indices of all requests
def requests_to_couples(requests):
    couples=[]
    for req in requests:
        couples.append((int(req[0].index),int(req[1].index)))
    return couples

# node_index is the indices of all nodes
def couples_to_node_index(couples):
    return [item for sublist in couples for item in sublist]

# p_couples is the population of couples, N is the population size
def create_p_couples(couples, N=5):
    p_couples = [None] * N
    for i in range(N):
        p_couples[i] = np.random.permutation(couples).tolist()
        #p_couples[i] = [tuple(l) for l in p_couples[i]] # to tuple
    return p_couples


# p_vehicle  is the population of vehicles, N is the population size
def create_p_vehicles(couples, N=5, max_vehicles=100, restricted_requests = 1000):
    # actually we have unlimited vehicles, but let's be realistic here
    # no retricted_requests for now
    p_vehicle = [None]*N # the initial population (size=N)
    for i in range (N):
        p_vehicle[i] = [0]*max_vehicles
        remain = len(couples)
        vehicle_index = 0
        while (remain>0):
            # couples_visited is the numbers of couples visited by that vehicle
            couples_visited = randint(1, remain)
            couples_visited = min(remain,couples_visited)
            p_vehicle[i][vehicle_index] = (couples_visited)
            #p_vehicle[i].append(couples_visited)
            vehicle_index +=1
            remain -= couples_visited
        p_vehicle[i].sort(reverse = True)

        #strip out all useless zeros!!!
        p_vehicle[i] = list(filter(lambda a: a != 0, p_vehicle[i]))
    return p_vehicle



# p_node is the population of nodes, N is the population size
def create_p_nodes(couples, N=5):
    nodes = couples_to_node_index(couples)
    p_node = [None] * N
    for i in range(N):
        p_node[i] = np.random.permutation(nodes).tolist()
        precedence_correction(p_node[i],couples)
    return p_node


# final population!!!
def create_p_tours(p_couples_vehicles,nodes,durations, N=5):
    # 'p_couples_vehicles' is an array of p_coup_veh of couples
    p_tours = [None]*len(p_couples_vehicles) * N
    i = 0
    for p_coup_veh in p_couples_vehicles:
        num_vehicles = len(p_coup_veh)
        for _ in range (N):
            p_tours[i] = [None] * num_vehicles
            j = 0
            for couples in p_coup_veh:
                nodes_index = couples_to_node_index(couples)
                tour = np.random.permutation(nodes_index).tolist()
                #tour = sort_by_ET(tour,nodes)
                #tour = sort_by_mean_time(tour,nodes)
                tour = precedence_correction(tour, couples)
                ######################tour = time_correction(tour,couples,durations,nodes)
                #time_violated = time_violated_nodes(tour,durations,couples,nodes)
                p_tours[i][j] = tour
                #print(time_violated)
                j += 1
            i += 1
    return p_tours

# create p_couples_vehicles, representing vehicles visiting couples
# 'p_couples' has sex with 'p_vehicles'
def create_p_couples_vehicles(p_couples,p_vehicles):
    res = [None]*len(p_vehicles)*len(p_couples) # the result will be size N1*N2
    i = 0
    for couples in p_couples:
        for vehicles in p_vehicles:
            pos = 0
            res[i] = [None]*len(vehicles)
            j = 0
            for num in vehicles:
                res[i][j] = couples[pos:(pos+num)]
                pos += num
                j += 1
            i += 1
    return res

def sort_by_ET(tour,nodes):
    ET = [nodes[i].ET for i in tour]
    res = [x for _, x in sorted(zip(ET, tour))]
    return res

def sort_by_LT(tour,nodes):
    LT = [nodes[i].LT for i in tour]
    res = [x for _, x in sorted(zip(LT, tour))]
    return res

def sort_by_mean_time(tour,nodes):
    mean_time = [nodes[i].LT+nodes[i].ET for i in tour]
    res = [x for _, x in sorted(zip(mean_time, tour))]
    return res

def job_distance(job,distances):
    if len(job) <= 0: return 0
    d = 0
    last_node = int(job[-1])
    n = len(job)
    for i in range(n-1):
        d += distances[job[i]][job[i+1]]
    d += distances[job[0]][last_node] # complete the circle
    return d

def total_distances(jobs,distances):
    d = 0
    for job in jobs:
        d += job_distance(job,distances)
    return d


def precedence_correction(tour, couples):
    visited = []
    for i in range(len(tour)):
        v = tour[i]
        couple = [item for item in couples if v in item][0]
        pickup = couple[0] # pickup node
        delivery = couple[1] # delivery node
        if (v == delivery): # v is delivery
            if (not pickup in visited): # the pickup node is not visited
                pickup_index = tour.index(pickup)
                tour.pop(pickup_index)
                tour.insert(i, pickup)
                visited.append(pickup)
                visited.append(v)
            else: # the sibling is visited
                visited.append(v)
        else: # v is pickup
            visited.append(v)
    return tour



def time_violated_index(tour,durations,nodes):
    cur_time = 0
    for i in range(len(tour) - 1):
        # print(len(nodes))
        # print (tour[i])
        cur_ET = nodes[tour[i]].ET
        cur_LT = nodes[tour[i]].LT
        next_ET = nodes[tour[i + 1]].ET
        next_LT = nodes[tour[i + 1]].LT
        time_arrived = cur_time + durations[tour[i]][tour[i + 1]]
        if (time_arrived > next_LT):  # VIOLATED!!!!!
            return i + 1
        cur_time = max(time_arrived, next_ET)
    return -1

def time_violated_nodes(tour,durations,couples,nodes):
    res = []
    index = []
    # if (len(tour) == 0):
    #     print ('BUGGGG!!!!!!!!!!!!!!!')
    #     return res
    cur_time = 0
    # print (tour)
    # print (cur_time)
    for i in range(len(tour) - 1):
        cur_pos = tour[i]
        next_pos = tour[i+1]

        cur_ET = nodes[cur_pos].ET
        cur_LT = nodes[cur_pos].LT
        next_ET = nodes[next_pos].ET
        next_LT = nodes[next_pos].LT
        cur_time = max(cur_time, cur_ET)
        time_arrived = cur_time + durations[cur_pos][next_pos]

        if (time_arrived > next_LT):  # VIOLATED!!!!!
            # debug ---------------------------------------
            print('################ Voilated!!! ####################')
            print(str(cur_pos) + '->' + str(next_pos))
            print('Arrived at '+str(time_arrived))
            print('ET='+str(next_ET)+',LT='+str(next_LT))

            v = tour.pop(i+1)
            print ('pop ' +str(v))
            print('#####################################################################')
            if (time_correction(v,tour,nodes,durations) >= 0):
                res.append(v)
                print('Append ' + str(v))
                i -= 1
            ######################
            next_ET = nodes[tour[i + 1]].ET
            next_LT = nodes[tour[i + 1]].LT
            time_arrived = cur_time + durations[tour[i]][tour[i + 1]]
            i += 1
            ##################

    for x in index :
        res.append(tour[x])
    for v in res:
        if (nodes[v].req_type =='p'):
            d_sib = nodes[v].d_sib
            print ('v ='+str(v))
            print('dsib ='+str(d_sib))
            print(tour)
            temp = tour.index(d_sib)
            index.append(temp)
            res.append(tour[temp])

        else :
            p_sib = nodes[v].p_sib
            temp = tour.index(p_sib)
            index.append(temp)
            res.append(tour[temp])
    for x in index:
        tour.pop(x)
    return res

def time_correction(v,tour,nodes,durations):
    cur_time = 0
    cur_ET = nodes[v].ET
    cur_LT = nodes[v].LT

    # case1 : pickup node
    if (nodes[v].req_type =='p'):
        d_sib = nodes[v].d_sib
        start = 0
        stop = tour.index(d_sib)

    # case 2: delivery node
    else:
        p_sib = nodes[v].p_sib
        start = tour.index(p_sib)
        stop = len(tour) - 1

    if (start > 0):
        cur_time = current_duration(tour,nodes,durations,start-1)

    # special case !! v should be first node
    if (cur_ET+durations[v][tour[0]] <=nodes[tour[0]].LT):
        return -1

    for i in range (start,stop):
        prev = tour[i]
        next = tour[i+1]
        prev_ET = nodes[prev].ET
        prev_LT = nodes[prev].LT
        next_ET = nodes[next].ET
        next_LT = nodes[next].LT
        cur_arrive = cur_time + durations[prev][v]
        if (cur_arrive > cur_LT):
            pass
        cur_arrive = max(cur_arrive,cur_ET)
        next_arrive = cur_arrive + durations[v][next]
        if (next_arrive <= next_LT):
            tour.insert(i,v)
            return -1
        cur_time += durations[prev][next]
        cur_time = max(cur_time,next_ET)
    # cannot insert
    return v

def current_duration(tour,nodes,durations,stop) :
    cur_time = nodes[tour[0]].ET
    for i in range(0,stop - 1):
        cur_time += durations[tour[i]][tour[i+1]]
        cur_time = max(cur_time,nodes[tour[i+1]].ET)
    return cur_time

def pickup_sibling(index,couples):
    sib = [item[0] for item in couples if index in item]
    return sib[0]

def delivery_sibling(index,couples):
    sib = [item[1] for item in couples if index in item]
    return sib[0]



# eval distance of all p_jobs
def eval_distance (p_jobs,distances,depot,nodes):
    res = []
    for tours in p_jobs:
        res.append(tours_distance(tours,distances,depot,nodes))
    return res

# distance of 'tours' by all vehicles
def tours_distance(tours, distances, depot,nodes):
    dist = 0
    for tour in tours:
        dist += tour_distance(tour,distances,depot,nodes)

    return dist

# distance of just one 'job' by one vehicle
def tour_distance(tour,distances,depot,nodes):
    dist = 0
    for i in range(len(tour)-1):
        dist += distances[tour[i]][tour[i+1]]

    dist += processing.distance(nodes[tour[0]],depot)+processing.distance(nodes[tour[-1]],depot)
    return dist



## below is junk !!!
'''
def set_files(fn):
    #print (fn)
    filename = fn
    nodes = tuple(preprocessing.load_node(filename))
    requests = preprocessing.generate_request(nodes)
    distances = processing.create_distance_table(nodes)


def jobs_to_chromosome(jobs,nodes):
    max_vehicles = len(nodes)-1
    chromosome = [None] * max_vehicles
    for i in range(len(jobs)):
        chromosome[i]=jobs[i]
    return chromosome

def clusters_to_jobs(clusters):
    jobs = [] # array of integer!!!
    for cluster in clusters:
        jobs.append(cluster_to_job(cluster))
    return jobs

def cluster_to_job(cluster):
    job=[]
    for req in cluster:
        job.append(int(req[0].index))
        job.append(int(req[1].index))
    return job

'''