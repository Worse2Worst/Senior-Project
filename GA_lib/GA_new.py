import os
import time
import numpy as np
import random
from random import randrange,randint,sample,choice
from pdp_lib import preprocessing
from pdp_lib import save_pics
from pdp_lib import util
from pdp_lib import processing



# A couple is the indices of all requests
def requests_to_couples(requests):
    couples=[]
    for req in requests:
        couples.append((int(req[0].index),int(req[1].index)))
    return couples

# node_index is the indices of all nodes
def couples_to_node_index(couples):
    return [item for sublist in couples for item in sublist]

def initialize_chromosome(num_vehicles = 25):
    chromosome =[[car_num,[]] for car_num in range(num_vehicles)]
    return chromosome


def new_tour_after_insert_requests(req,tour,nodes,distances,durations):
    candidates = []
    if(len(tour)==0):
        return [req[0],req[1]]
    # generate all possibilities of insertions
    new_vehicle_dist = eval.tour_distance(req, distances)
    old_tour_dist =  eval.tour_distance(tour,distances)
    for i in range(len(tour)+1):
        temp1 = tour[:]
        temp1.insert(i,req[0])
        for j in range(i+1,len(temp1)+1):
            temp2 = temp1[:]
            temp2.insert(j,req[1])
            # now remove the bad ones
            # Assume that precedence not violated
            if (not time_violated(temp2,nodes,durations)):
                candidates.append(temp2)
    # if no feasible paths!!!, return empty
    if(len(candidates) ==0):
        return []
    # select the best candidates
    min_dist = 99999999999999999
    min_index = -999
    for i in range(len(candidates)):
        dist = eval.tour_distance(candidates[i],distances)
        if(dist<min_dist):
            min_dist = dist
            min_index = i
    # if inserting can reduce cost, then insert
    if(min_dist - old_tour_dist < new_vehicle_dist):
        return candidates[min_index]
    # else, just don't insert and return empty
    return []

# To tell whether the time-window is violated, True is violated, False is OK
def time_violated(tour,nodes,durations):
    cur_time = 0
    for i in range(len(tour)-1):
        cur_node = nodes[tour[i]]
        next_node = nodes[tour[i+1]]
        cur_ET = cur_node.ET
        next_LT = next_node.LT
        cur_time = max(cur_time,cur_ET)
        arrival_time = cur_time+durations[tour[i]][tour[i+1]]
        if(arrival_time > next_LT):
            return True
    return False

# To tell whether the precedence (pickup-delivery) is violated, True is violated, False is OK
def precedence_violated(tour, couples,nodes):
    visited = []
    for i in range(len(tour)):
        v = tour[i]
        req_type = nodes[v].req_type
        if (req_type == 'd'): # v is delivery
            pickup = nodes[v].p_sib
            if (not pickup in visited): # the pickup node is not visited
                return True
            else: # the sibling is visited
                visited.append(v)
        else: # v is pickup
            visited.append(v)
    return False