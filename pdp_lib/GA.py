import os
import time
from pdp_lib import preprocessing
from pdp_lib import save_pics
from pdp_lib import util
from pdp_lib import processing

def cluster_to_job(cluster):
    job=[]
    for req in cluster:
        job.append(req[0])
        job.append(req[1])
    return job

def job_distance(job):
    if len(job) <= 0: return 0
    distance = 0
    last_node = job[-1]
    n = len(job)
    for i in range(n-1):
        distance += processing.distance(job[i],job[i+1])
    distance += processing.distance(job[0],last_node) # complete the circle
    return distance

def total_distances(jobs):
    distances = 0
    for job in jobs:
        distances += job_distance(job)
    return distances

def precedence_correction(job):
    wrong_list = []
    visited = []
    carrier = 0
    for node in job:
        if node.req_type == 'p':
            visited.append(node)
        else: # node is delivery
            pickup_pair = pair_node(job,node)
            if (not pickup_pair in visited):
                wrong_list.append((node,node.index,pickup_pair.index))
            else:
                visited.append(node)
    i = 0
    for v in visited:
        for w in wrong_list:
            if (int(w[2]) == int(v.index)):
                visited.insert(i+1,w[0])
        i += 1

    job = visited
    return job

def pair_node(job,v):
    if v.req_type == 'p':
        index = int(v.d_sib)
    else:
        index = int(v.p_sib)
    for node in job:
        if (index == int(node.index)):
            return node

def swap(job,i,j):
    job[i],job[j]=job[j],job[i]